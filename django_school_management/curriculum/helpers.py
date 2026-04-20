"""
Helpers for using the curriculum library.

- get_subjects_for_level: subjects (templates) for a curriculum level and optional stream.
- suggest_subjects_for_institute: suggested subject templates for an institute's curriculum,
  class/semester, and optional department/stream.
"""

from django_school_management.curriculum.models import (
    Curriculum,
    CurriculumLevel,
    CurriculumSubject,
    SubjectTemplate,
)
from django.db import models


def get_subjects_for_level(curriculum, level_number, stream=None):
    """
    Return subject templates for a given curriculum, level number, and optional stream.

    - If stream is None: returns common subjects (CurriculumSubject.stream is null) for that level.
    - If stream is set: returns common subjects plus stream-specific subjects for that level.

    Args:
        curriculum: Curriculum instance or id.
        level_number: int (e.g. 9 for Class 9).
        stream: Stream instance, or code string ('Science', 'Arts', 'Commerce'), or None.

    Returns:
        QuerySet of SubjectTemplate (distinct), ordered by display_order.
    """
    if isinstance(curriculum, int):
        curriculum = Curriculum.objects.get(pk=curriculum)
    level = CurriculumLevel.objects.filter(
        curriculum=curriculum,
        level_number=level_number,
    ).first()
    if not level:
        return SubjectTemplate.objects.none()

    qs = CurriculumSubject.objects.filter(curriculum=curriculum, level=level).select_related(
        'subject_template', 'stream'
    )
    if stream is None:
        return SubjectTemplate.objects.filter(
            curriculum_subject_entries__curriculum=curriculum,
            curriculum_subject_entries__level=level,
            curriculum_subject_entries__stream__isnull=True,
        ).distinct().order_by('curriculum_subject_entries__display_order', 'display_order', 'name')
    # Resolve stream by code if string
    if isinstance(stream, str):
        from django_school_management.curriculum.models import Stream
        stream = Stream.objects.filter(code=stream).first()
    if not stream:
        return get_subjects_for_level(curriculum, level_number, stream=None)
    # Common (stream=null) + this stream
    common_ids = list(
        qs.filter(stream__isnull=True).values_list('subject_template_id', flat=True)
    )
    stream_ids = list(qs.filter(stream=stream).values_list('subject_template_id', flat=True))
    all_ids = list(dict.fromkeys(common_ids + stream_ids))
    return SubjectTemplate.objects.filter(pk__in=all_ids).order_by('display_order', 'name')


def suggest_subjects_for_institute(institute, semester_number, department=None):
    """
    Suggest subject templates for an institute given its curriculum, semester/class number,
    and optional department (group). Useful when building SubjectGroup or creating Subjects.

    - If institute has no curriculum: returns empty queryset.
    - Resolves level by curriculum level with matching semester_number (or level_number).
    - If curriculum level has streams_applicable and department maps to a stream (e.g. by name),
      returns common + stream-specific subjects; otherwise common only.

    Args:
        institute: InstituteProfile instance.
        semester_number: int (1–12), maps to Class/Semester number.
        department: optional Department (Group) instance; if name matches a Stream (Science/Arts/Commerce),
                    stream-specific subjects are included.

    Returns:
        QuerySet of SubjectTemplate.
    """
    if not getattr(institute, 'curriculum_id', None) or not institute.curriculum_id:
        return SubjectTemplate.objects.none()

    curriculum = institute.curriculum
    level = CurriculumLevel.objects.filter(
        curriculum=curriculum,
    ).filter(
        models.Q(semester_number=semester_number) | models.Q(level_number=semester_number)
    ).first()
    if not level:
        return SubjectTemplate.objects.none()

    stream = None
    if level.streams_applicable and department and getattr(department, 'name', None):
        from django_school_management.curriculum.models import Stream
        stream = Stream.objects.filter(
            code__iexact=department.name.strip()
        ).first()
    return get_subjects_for_level(curriculum, level.level_number, stream=stream)


def load_subjects_from_curriculum(institute, curriculum, class_numbers, created_by):
    """
    Create Semesters (if missing), Subjects from SubjectTemplates, and SubjectGroups
    for the given institute, curriculum, and class/semester numbers.

    - Ensures Semester exists for each number in class_numbers (1-12).
    - For each (department, semester_number): gets subject templates for that curriculum+level+stream
      (stream from department name when level has streams_applicable), get_or_creates Subject from
      each template, then get_or_creates SubjectGroup(department, semester) and sets its subjects.

    Args:
        institute: InstituteProfile instance (departments and curriculum used).
        curriculum: Curriculum instance (or None to use institute.curriculum).
        class_numbers: list of int (e.g. [1,2,3,4,5] or list(range(1,11))).
        created_by: User for Subject/Semester created_by.

    Returns:
        dict with 'semesters_created', 'subjects_created', 'subject_groups_created', 'errors' (list).
    """
    from django_school_management.academics.models import Semester, Subject
    from django_school_management.result.models import SubjectGroup

    curriculum = curriculum or getattr(institute, 'curriculum', None)
    if not curriculum:
        return {'semesters_created': 0, 'subjects_created': 0, 'subject_groups_created': 0, 'errors': ['No curriculum selected.']}

    departments = list(institute.departments.filter(institute=institute))
    if not departments:
        return {'semesters_created': 0, 'subjects_created': 0, 'subject_groups_created': 0, 'errors': ['No departments/groups found. Add them in the previous step.']}

    BASE_CODE = 10000  # avoid clash with existing subject_code
    semesters_created = 0
    subjects_created = 0
    subject_groups_created = 0
    errors = []

    for num in class_numbers:
        if 1 <= num <= 12:
            sem, created = Semester.objects.get_or_create(
                number=num,
                defaults={'created_by': created_by},
            )
            if created:
                semesters_created += 1

    for dept in departments:
        for sem_num in class_numbers:
            if sem_num < 1 or sem_num > 12:
                continue
            try:
                semester = Semester.objects.get(number=sem_num)
            except Semester.DoesNotExist:
                errors.append(f'Semester {sem_num} not found.')
                continue
            templates = get_subjects_for_level(
                curriculum, sem_num,
                stream=dept.name.strip() if dept.name else None,
            )
            if not templates:
                continue
            subject_pks = []
            for template in templates:
                subject_code = BASE_CODE + template.pk
                subject, created = Subject.objects.get_or_create(
                    subject_template=template,
                    defaults={
                        'name': template.name[:50],
                        'subject_code': subject_code,
                        'theory_marks': template.default_theory_marks,
                        'practical_marks': template.default_practical_marks,
                        'created_by': created_by,
                    },
                )
                if created:
                    subjects_created += 1
                subject_pks.append(subject.pk)
            sg, created = SubjectGroup.objects.get_or_create(
                department=dept,
                semester=semester,
                defaults={},
            )
            for pk in subject_pks:
                sg.subjects.add(pk)
            if created:
                subject_groups_created += 1
    return {
        'semesters_created': semesters_created,
        'subjects_created': subjects_created,
        'subject_groups_created': subject_groups_created,
        'errors': errors,
    }
