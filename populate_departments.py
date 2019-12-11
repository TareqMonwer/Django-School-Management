import django
import os
# must be in top of django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
# must come after django.setup()
from admin_tools.models import Department

depts = [
    'Computer', 'Civil', 'Telecom',
    'Medical', 'AIDT', 'Textile',
    'Tourism and Hospitality', 'Electrical'
]

for dept in depts:
    dept = Department.objects.get_or_create(name=dept)
