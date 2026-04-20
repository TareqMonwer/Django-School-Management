import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError

from django_school_management.accounts.models import User
from django_school_management.institute.models import InstituteProfile
from django_school_management.academics.models import (
    AcademicSession,
    Batch,
    Department,
    Semester,
)
from django_school_management.students.models import AdmissionStudent, Student


class Command(BaseCommand):
    help = "Seed database with realistic data for performance/load tests."

    def add_arguments(self, parser):
        parser.add_argument(
            "--admissions",
            type=int,
            default=20000,
            help="Target number of AdmissionStudent rows (default: 20000)",
        )
        parser.add_argument(
            "--students",
            type=int,
            default=2000,
            help="Target number of enrolled Student rows (default: 2000)",
        )

    def handle(self, *args, **options):
        admissions_target = max(0, options["admissions"])
        students_target = max(0, options["students"])

        institute = InstituteProfile.objects.filter(active=True).first()
        if not institute:
            raise CommandError(
                "No active InstituteProfile found. "
                "Please create and configure an active institute before seeding."
            )

        self.stdout.write(self.style.NOTICE(f"Using institute: {institute} (id={institute.id})"))

        # Academic session for current year (creator can be null for seed data).
        current_year = date.today().year
        session, _ = AcademicSession.objects.get_or_create(
            year=current_year,
            defaults={"created_by": None},
        )
        self.stdout.write(self.style.NOTICE(f"Using academic session: {session}"))

        # Ensure at least a few departments for this institute.
        depts = list(Department.objects.filter(institute=institute))
        if not depts:
            self.stdout.write(self.style.NOTICE("No departments found; creating seed departments."))
            for i in range(1, 4):
                dept = Department.objects.create(
                    name=f"Perf Dept {i}",
                    short_name=f"P{i}",
                    code=100 + i,
                    institute=institute,
                    created_by=None,
                )
                depts.append(dept)

        # Ensure at least one semester (1st) exists.
        default_semester, _ = Semester.objects.get_or_create(
            number=1,
            defaults={"created_by": None},
        )

        # Ensure at least one batch per department for the current session.
        batches_by_dept = {}
        for dept in depts:
            batch, _ = Batch.objects.get_or_create(
                year=session,
                department=dept,
                number=1,
            )
            batches_by_dept[dept.id] = batch

        # Ensure at least one staff user for performance tests.
        if not User.objects.filter(username="perf_admin").exists():
            User.objects.create_superuser(
                username="perf_admin",
                email="perf_admin@example.com",
                password="perf_admin",
                requested_role="admin",
                institute=institute,
            )
            self.stdout.write(self.style.NOTICE("Created superuser 'perf_admin' with password 'perf_admin'."))

        # Seed AdmissionStudent entries up to the requested target.
        existing_admissions = AdmissionStudent.objects.count()
        to_create = max(0, admissions_target - existing_admissions)
        if to_create:
            self.stdout.write(
                self.style.NOTICE(
                    f"Existing AdmissionStudent rows: {existing_admissions}. "
                    f"Creating additional {to_create} entries to reach {admissions_target}."
                )
            )
            self._bulk_create_admissions(to_create, depts)
        else:
            self.stdout.write(
                self.style.NOTICE(
                    f"AdmissionStudent rows ({existing_admissions}) already meet or exceed target ({admissions_target})."
                )
            )

        # Seed enrolled Student rows for a subset of admitted+paid applicants.
        existing_students = Student.objects.count()
        remaining_students = max(0, students_target - existing_students)
        if remaining_students:
            self.stdout.write(
                self.style.NOTICE(
                    f"Existing Student rows: {existing_students}. "
                    f"Creating up to {remaining_students} new students using admitted+paid applicants."
                )
            )
            self._create_students_from_admissions(
                remaining_students,
                session,
                default_semester,
                batches_by_dept,
            )
        else:
            self.stdout.write(
                self.style.NOTICE(
                    f"Student rows ({existing_students}) already meet or exceed target ({students_target})."
                )
            )

        self.stdout.write(self.style.SUCCESS("Performance data seeding complete."))

    def _bulk_create_admissions(self, count, depts):
        """Efficiently create many AdmissionStudent rows without heavy validation."""
        objs = []
        batch_size = 2000
        today = date.today()

        for i in range(count):
            dept = random.choice(depts)
            index = AdmissionStudent.objects.count() + i + 1

            # Rough distribution:
            # - 50% paid
            # - 25% admitted (subset of paid)
            # - 10% rejected
            paid = (i % 2 == 0)
            admitted = paid and (i % 4 == 0)
            rejected = (i % 10 == 0)

            obj = AdmissionStudent(
                name=f"Applicant {index}",
                fathers_name="Father Name",
                mothers_name="Mother Name",
                date_of_birth=today - timedelta(days=6000),
                email=f"applicant_{index}@example.com",
                current_address="Performance Seed Address",
                permanent_address="Performance Seed Address",
                mobile_number="01700000000",
                guardian_mobile_number="01700000001",
                department_choice=dept,
                paid=paid,
                admitted=admitted,
                admission_date=today if admitted else None,
                rejected=rejected,
                application_type="1",
            )
            objs.append(obj)

            if len(objs) >= batch_size:
                AdmissionStudent.objects.bulk_create(objs, batch_size=batch_size)
                objs = []

        if objs:
            AdmissionStudent.objects.bulk_create(objs, batch_size=batch_size)

    def _create_students_from_admissions(
        self,
        max_to_create,
        session,
        default_semester,
        batches_by_dept,
    ):
        """
        Create Student rows from admitted+paid applicants that are not yet assigned.

        Uses normal .create() so that Student.save() business rules (temp IDs, flags)
        are respected.
        """
        # Only use applicants that are fully admitted and paid, not yet converted.
        candidates = (
            AdmissionStudent.objects.filter(
                admitted=True,
                paid=True,
                rejected=False,
                assigned_as_student=False,
                choosen_department__isnull=False,
            )
            .select_related("choosen_department")
            .order_by("id")[:max_to_create]
        )

        created_count = 0
        for registrant in candidates:
            dept = registrant.choosen_department
            batch = batches_by_dept.get(dept.id)
            if not batch:
                # Safety: should not happen, but avoid crashes in seed command.
                batch, _ = Batch.objects.get_or_create(
                    year=session,
                    department=dept,
                    number=1,
                )
                batches_by_dept[dept.id] = batch

            Student.objects.create(
                admission_student=registrant,
                semester=default_semester,
                ac_session=session,
                batch=batch,
                admitted_by=None,
            )
            created_count += 1

        self.stdout.write(
            self.style.NOTICE(f"Created {created_count} Student rows from admitted+paid applicants.")
        )

