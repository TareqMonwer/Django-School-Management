from django.shortcuts import render

from admin_tools.models import Semester
from students.models import Student
from result.models import Result


def show_result_by_semester(request, student_id, semester):
    student = Student.objects.get(pk=student_id)
    semester = Semester.objects.get(number=semester)
    results = Result.objects.filter(student_id=student_id,
                                    semester=semester)
    context = {'results': results, 'student': student}
    return render(request, 'students/result_in_detail.html', context)
