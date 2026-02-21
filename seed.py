import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from rolepermissions.roles import AbstractUserRole
from django.conf import settings

for role in AbstractUserRole.__subclasses__():
    role.get_or_create_group()

from django_school_management.institute.models import City
if not City.objects.filter(country='BD').exists():
    call_command('loaddata', 'bd_cities.json', verbosity=1)
    print("Loaded Bangladesh cities fixture.")
else:
    print("Bangladesh cities already loaded, skipping.")

if settings.IS_DEMO_ENV:
    from django.contrib.auth import get_user_model

    User = get_user_model()

    if not User.objects.filter(username=settings.DEMO_SUPERUSER_USERNAME).exists():
        demo_superuser = User.objects.create_superuser(
            username=settings.DEMO_SUPERUSER_USERNAME,
            email=settings.DEMO_SUPERUSER_EMAIL,
            password=settings.DEMO_SUPERUSER_PASSWORD,
        )
        print(f"Demo superuser created: {demo_superuser}")
        print(f"Demo superuser username: {settings.DEMO_SUPERUSER_USERNAME}")
        print(f"Demo superuser email: {settings.DEMO_SUPERUSER_EMAIL}")
        print(f"Demo superuser password: {settings.DEMO_SUPERUSER_PASSWORD}")
    else:
        print("Demo superuser already exists, skipping.")

