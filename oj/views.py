from django.utils import timezone
import filecmp
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
import os
from .models import Problems, Solutions
import tempfile

def problems(request):
    problems_list = Problems.objects.all()
    context = {'problem_list':problems_list}
    return render(request, 'oj/index.html', context)

def problemDetail(request, problem_id):
    problem = get_object_or_404(Problems, pk=problem_id)
    context = {'problem': problem}
    return render(request, 'oj/detail.html', context)

def submitCode(request, problem_id):
    codeText = request.POST.get('textsolution')

    tempSolution = tempfile.NamedTemporaryFile(suffix=".cpp")
    tempSolution.write(str.encode(codeText))
    tempSolution.seek(0)
    
    os.system('g++ ' + tempSolution.name)
    os.system('./a.out < codeRunner/inp.txt > codeRunner/out.txt')
    tempSolution.close()

    out1 = 'codeRunner/out.txt'
    out2 = 'codeRunner/actual_out.txt'

    if(filecmp.cmp(out1, out2, shallow=False)):
        verdict = 'Accepted'
    else:
        verdict = 'Wrong Answer'

    solution = Solutions()
    solution.problem = Problems.objects.get(pk=problem_id)
    solution.verdict = verdict
    solution.submitted_at = timezone.now()
    solution.submitted_code = codeText
    solution.save()

    return redirect('oj:submissions')


def submissions(request):
    submission = Solutions.objects.all()
    context = {'submission': submission}
    return render(request, 'oj/submissions.html', context)