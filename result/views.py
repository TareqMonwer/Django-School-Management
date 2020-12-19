from django.shortcuts import render

from .models import Result
from .filters import ResultFilter


def result_view(request):
    f = ResultFilter(request.GET, queryset=Result.objects.all())
    ctx = {'filter': f,}
    return render(request, 'result/result_filter.html', ctx)


def result_detail_view(request, student_pk):
    return render(request, 'result/result_detail.html')
