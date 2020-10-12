from django.shortcuts import render, redirect
from students.forms import StudentForm
from students.models import AdmissionStudent


def index(request):
    return render(request, 'landing/index.html')


def online_admission(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()
            print(data)
            return redirect('students:all_student')
    else:
        form = StudentForm()
    return render(request, 'pages/students/admission.html', {'form': form})
