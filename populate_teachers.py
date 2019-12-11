import random
import django
import os
# must be on top of django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from faker import Faker

# must come after django setup()
from teachers.models import Teacher, Designation


fakegen = Faker()


def create_designations():
    designations = [
        'Instructor', 'Sr. Instructor', 'Jr. Instructor',
        'Asst. Instructor', 'Lecturer',
    ]
    for des in designations:
        Designation.objects.get_or_create(title=des)


create_designations()

# designations
designations = []
for i in range(1, 6):
    des = Designation.objects.get(id=i)
    designations.append(des)

def generate_teacher(n=10):
    for entry in range(n):
        name = fakegen.name()
        des = random.choice(designations)
        mobile = fakegen.phone_number()
        email = fakegen.email()

        try:
            teacher = Teacher.objects.get_or_create(
                name=name,
                designation=des,
                mobile=mobile,
                email=email)
        except:
            continue
        
        


if __name__ == "__main__":
    print('Creating Fake Teachers....')
    n = int(input('How many teachers do you wanna create?'))
    generate_teacher(n)
    print('teachers created successfully.')
