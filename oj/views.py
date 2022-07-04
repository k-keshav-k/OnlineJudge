from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Problems, Solutions

def problems(request):
    problems_list = Problems.objects.all()
    context = {'problem_list':problems_list}
    return render(request, 'oj/index.html', context)

def problemDetail(request, problem_id):
    problem = get_object_or_404(Problems, pk=problem_id)
    context = {'problem': problem}
    return render(request, 'oj/detail.html', context)