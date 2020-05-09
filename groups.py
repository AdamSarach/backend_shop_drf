import os
import django

from django.contrib.auth.models import Group

'''Add user groups to Group Model when new db is created by code in console $ python groups.py'''

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

GROUPS = ['admin', 'employee', 'customer']
MODELS = ['user']

for group in GROUPS:
    new_group, created = Group.objects.get_or_create(name=group)
