from django.shortcuts import render
from django.http import HttpResponse


def online_admission(request):
    return HttpResponse('Online Admission Form')
