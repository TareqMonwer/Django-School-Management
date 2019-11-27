from django.db import models


class Designation(models.Model):
    title = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Topic(models.Model):
    name = models.CharField(max_length=200)
    added_in = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Teacher(models.Model):
    name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='teachers', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    expertise = models.ManyToManyField(
        to=Topic, blank=True, related_name='expert_in')
    mobile = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    joining_date = models.DateField(auto_now=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.designation)
