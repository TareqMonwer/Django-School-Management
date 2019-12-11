import random
import django
import os
# must be in top of django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from faker import Faker
# must come after django.setup()
from admin_tools.models import Department, Semester, AcademicSession
from students.models import Student


fakegen = Faker()


# get the academmic_session
ac_session = AcademicSession.objects.get(year=2017)

# 1-8th semester objects
sems = []
for i in range(1, 9):
    sems.append(Semester.objects.get(number=i))


# some departments
depts = []
for i in range(1, 7):
    depts.append(Department.objects.get(pk=i))


def generate_students(n=10,semester=None, department=None):
    for entry in range(n):
        name = fakegen.name()
        roll = fakegen.random_int(min=10000, max=99999, step=1)
        regi = fakegen.random_int(min=10000, max=99999, step=1)
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
    generate_students(n)
    print('students are created.')
