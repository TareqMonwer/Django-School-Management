from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
import json

from django_school_management.students.models import Student
from django_school_management.academics.models import Semester, Subject, Department
from .models import Result, SubjectGroup
from .filters import ResultFilter, SubjectGroupFilter
from permission_handlers.basic import user_is_verified
from permission_handlers.administrative import user_is_teacher_or_administrative


@user_passes_test(user_is_verified)
def result_view(request):
    if not request.GET:
        qs = Result.objects.none()
    else:
        qs = Result.objects.all()
    f = ResultFilter(request.GET, queryset=qs, request=request)
    ctx = {'filter': f, }
    return render(request, 'result/result_filter.html', ctx)


@user_passes_test(user_is_verified)
def result_detail_view(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    student_results = student.results.all()
    semesters = list(Semester.objects.all())
    semester_results = {}
    active_semesters = []

    for semester in semesters:
        results = student_results.filter(semester=semester)
        if results:
            active_semesters.append(semester)
            semester_results.update(
                {f'{semester}': results}
            )
    ctx = {
        'student': student,
        'semester_results': semester_results,
        'active_semesters': active_semesters
    }
    return render(request, 'result/result_detail.html', ctx)


def find_student(request, student_id):
    """ Find student by given id for result entry."""
    student = Student.objects.get(
        temporary_id=student_id
    )
    ctx = {
        'student_name': student.admission_student.name,
        'student_batch': student.batch.number,
        'image_url': student.admission_student.photo.url
    }
    return JsonResponse({'data': ctx})


@user_passes_test(user_is_teacher_or_administrative)
def result_entry(request):
    if not request.GET:
        qs = SubjectGroup.objects.none()
    else:
        qs = SubjectGroup.objects.all()

    subject_group_filter = SubjectGroupFilter(
        request.GET,
        queryset=qs,
        request=request
    )

    if request.method == 'POST':
        data_items = request.POST.items()
        # get student from pk
        student_temp_id = request.POST.get('student_id')
        student = Student.objects.get(temporary_id=student_temp_id)
        semester = Semester.objects.get(pk=int(request.POST.get('semester')))

        result_created = {}
        for key, value in data_items:
            # get subject from pk
            if '.' in key:
                try:
                    s_pk = int(key.split('.')[1])
                    subject = Subject.objects.get(pk=s_pk)
                    if not result_created.get(str(s_pk)):
                        # get subject marks
                        practical_marks = int(
                            request.POST.get(f'practical_marks.{s_pk}')
                        )
                        theory_marks = int(
                            request.POST.get(f'theory_marks.{s_pk}')
                        )
                        result = Result(
                            student=student,
                            semester=semester,
                            subject=subject,
                            practical_marks=practical_marks,
                            theory_marks=theory_marks
                        )
                        try:
                            result.save()
                            result_created[str(s_pk)] = True
                        except IntegrityError:
                            messages.error(
                                request,
                                f'{student.admission_student.name}\'s result '
                                f'for {subject} has been created already.'
                            )
                except ValueError:
                    pass
        return redirect('result:result_entry')
    ctx = {
        'subject_group_filter': subject_group_filter,
    }
    return render(request, 'result/result_entry.html', ctx)


@user_passes_test(user_is_teacher_or_administrative)
def create_subject_group(request):
    departments = Department.objects.all()
    semesters = Semester.objects.all()
    subjects = Subject.objects.all()
    copy_from_group = None
    copy_from_subject_pks = []

    copy_from_pk = request.GET.get('copy_from')
    if copy_from_pk:
        try:
            copy_from_group = SubjectGroup.objects.get(pk=copy_from_pk)
            copy_from_subject_pks = list(
                copy_from_group.subjects.values_list('pk', flat=True)
            )
        except (SubjectGroup.DoesNotExist, ValueError):
            pass

    if request.method == 'POST':
        dept_pk = request.POST.get('department')
        subject_list = request.POST.getlist('subject')
        semester_pk = request.POST.get('semester')

        if dept_pk and semester_pk is not None:
            dept = Department.objects.get(pk=dept_pk)
            semester = Semester.objects.get(pk=semester_pk)

            subject_group = SubjectGroup.objects.create(
                department=dept,
                semester=semester
            )

            for s_pk in subject_list:
                try:
                    subj = Subject.objects.get(pk=int(s_pk))
                    subject_group.subjects.add(subj)
                except (Subject.DoesNotExist, ValueError):
                    pass

            subject_group.save()
            messages.success(request, 'Subject group created.')
            return redirect('result:subject_groups')

    ctx = {
        'departments': departments,
        'semesters': semesters,
        'subjects': subjects,
        'copy_from_group': copy_from_group,
        'copy_from_subject_pks': copy_from_subject_pks,
        'copy_from_subject_pks_json': json.dumps(copy_from_subject_pks),
        'existing_subject_groups': SubjectGroup.objects.select_related(
            'department', 'semester'
        ).order_by('department__name', 'semester__number')[:50],
    }
    return render(request, 'result/create_subject_groups.html', ctx)


@user_passes_test(user_is_verified)
def subject_group_list(request):
    subject_groups = SubjectGroup.objects.all()
    ctx = {
        'subject_groups': subject_groups,
    }
    return render(request, 'result/subject_group_list.html', ctx)
