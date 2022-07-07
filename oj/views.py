from django.utils import timezone
import filecmp
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
import os
from .models import Problems, Solutions

def problems(request):
    problems_list = Problems.objects.all()
    context = {'problem_list':problems_list}
    return render(request, 'oj/index.html', context)

def problemDetail(request, problem_id):
    problem = get_object_or_404(Problems, pk=problem_id)
    context = {'problem': problem}
    return render(request, 'oj/detail.html', context)

def submitCode(request, problem_id):
    f = request.FILES['solution']
    with open('D:/onlineJudge_dir/onlineJudge/codeRunner/solution.cpp', 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
        
    sol = open('D:/onlineJudge_dir/onlineJudge/codeRunner/solution.cpp', "r")
    os.system('g++ D:/onlineJudge_dir/onlineJudge/codeRunner/solution.cpp')
    os.system('a.exe < D:/onlineJudge_dir/onlineJudge/codeRunner/inp.txt > D:/onlineJudge_dir/onlineJudge/codeRunner/out.txt')

    out1 = 'D:/onlineJudge_dir/onlineJudge/codeRunner/out.txt'
    out2 = 'D:/onlineJudge_dir/onlineJudge/codeRunner/actual_out.txt'

    if(filecmp.cmp(out1, out2, shallow=False)):
        verdict = 'Accepted'
    else:
        verdict = 'Wrong Answer'

    solution = Solutions()
    solution.problem = Problems.objects.get(pk=problem_id)
    solution.verdict = verdict
    solution.submitted_at = timezone.now()
    solution.submitted_code = sol.read()
    solution.save()

    return HttpResponse(verdict)