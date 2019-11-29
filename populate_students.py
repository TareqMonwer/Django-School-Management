import random
import django
django.setup()
from faker import Faker
from admin_tools.models import Department, Semester, AcademicSession
from students.models import Student
import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


fakegen = Faker()


# Get some departments
dept1 = Department.objects.get(pk=1)
dept2 = Department.objects.get(pk=2)
dept3 = Department.objects.get(pk=3)
dept4 = Department.objects.get(pk=4)
dept5 = Department.objects.get(pk=5)
dept6 = Department.objects.get(pk=6)

# Get some semesters
sem1 = Semester.objects.get(number=1)
sem2 = Semester.objects.get(number=2)
sem3 = Semester.objects.get(number=3)
sem4 = Semester.objects.get(number=4)
sem5 = Semester.objects.get(number=5)
sem6 = Semester.objects.get(number=6)
sem7 = Semester.objects.get(number=7)
sem8 = Semester.objects.get(number=8)

# get the session
ac_session = AcademicSession.objects.get(year=2019)

sems = [sem1, sem2, sem3, sem4, sem5, sem6, sem7, sem8]
depts = [dept1, dept2, dept3, dept4, dept5, dept6]


def generate_students(n=10,semester=None, department=None):
    for entry in range(n):
        name = fakegen.name()
        roll = fakegen.random_int(min=10000, max=10000, step=1)
        regi = fakegen.random_int(min=10000, max=9000000, step=1)
        dept = random.choice(depts)
        sem = random.choice(sems)
        mobile = fakegen.phone_number()
        guardian = fakegen.phone_number()

        try:
            if semester and department:
                student = Student.objects.get_or_create(
                name=name,
                roll=roll,
                registration_number=regi,
                department=dept,
                semester=semester,
                mobile=mobile,
                guardian_mobile=guardian)
            else:
                student = Student.objects.get_or_create(
                name=name,
                roll=roll,
                registration_number=regi,
                department=dept,
                semester=sem,
                mobile=mobile,
                guardian_mobile=guardian)
        except:
            continue
        
        


if __name__ == "__main__":
    print('Creating Fake Students....')
    n = int(input('How many students do you wanna create?'))
    generate_students(n, semester=sem5, department=dept1)
    print('students are created.')
