from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings



class CustomGroup(Group):
    group_creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE)
    
    def display_group(self):
        return f'{self.name} created by {self.group_creator}'
