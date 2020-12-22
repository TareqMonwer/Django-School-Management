from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse

from students.models import Student
from academics.models import Semester, Subject
from .models import Result, SubjectGroup
from .filters import ResultFilter, SubjectGroupFilter


def result_view(request):
    if not request.GET:
        qs = Result.objects.none()
    else:
        qs = Result.objects.all()
    f = ResultFilter(request.GET, queryset=qs)
    ctx = {'filter': f, }
    return render(request, 'result/result_filter.html', ctx)


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


def result_entry(request):
    if not request.GET:
        qs = SubjectGroup.objects.none()
    else:
        qs = SubjectGroup.objects.all()

    subject_group_filter = SubjectGroupFilter(
        request.GET,
        queryset=qs
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
