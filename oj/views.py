from django.utils import timezone
import filecmp
from django.shortcuts import get_object_or_404, render, redirect
import os
from .models import Problems, Solutions, testCases
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

    tempOutput = tempfile.NamedTemporaryFile(suffix=".txt")
    tempOutput.seek(0)

    os.system('g++ ' + tempSolution.name + ' && ./a.out < codeRunner/inp.txt > ' + tempOutput.name)
    tempSolution.close()

    out2 = 'codeRunner/actual_out.txt'

    tempOutput.seek(0)
    if(filecmp.cmp(out2, tempOutput.name, shallow=False)):
        verdict = 'Accepted'
    else:
        verdict = 'Wrong Answer'

    tempOutput.close()

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