from django.utils import timezone
import filecmp
from django.shortcuts import get_object_or_404, render, redirect
import os
from .models import Problems, Solutions, testCases
import tempfile
from django.contrib.auth.decorators import login_required

@login_required
def problems(request):
    problems_list = Problems.objects.all()
    context = {'problem_list':problems_list}
    return render(request, 'oj/index.html', context)

@login_required
def problemDetail(request, problem_id):
    problem = get_object_or_404(Problems, pk=problem_id)
    context = {'problem': problem}
    return render(request, 'oj/detail.html', context)

@login_required
def submitCode(request, problem_id):
    codeText = request.POST.get('textsolution')

    tempSolution = tempfile.NamedTemporaryFile(suffix=".cpp")
    tempSolution.write(str.encode(codeText))
    tempSolution.seek(0)

    problem = get_object_or_404(Problems, pk=problem_id)

    inp = problem.testcases_set.all()

    os.system('g++ ' + tempSolution.name)

    tempSolution.close()

    for i in inp:
        tempOutput = tempfile.NamedTemporaryFile(suffix=".txt")
        tempOutput.seek(0)

        tempInput = tempfile.NamedTemporaryFile(suffix=".txt")
        tempInput.write(str.encode(i.input))

        tempInput.seek(0)
        os.system('./a.out < ' + tempInput.name + ' > ' + tempOutput.name)

        tempActualOutput = tempfile.NamedTemporaryFile(suffix=".txt")
        tempActualOutput.write(str.encode(i.output))

        tempOutput.seek(0)
        tempActualOutput.seek(0)
        print(tempActualOutput.read())
        print(tempOutput.read())
        if(filecmp.cmp(tempActualOutput.name, tempOutput.name, shallow=False)):
            verdict = 'Accepted'
        else:
            verdict = 'Wrong Answer'
            break

        tempOutput.close()
        tempActualOutput.close()
        tempInput.close()

    solution = Solutions()
    solution.problem = Problems.objects.get(pk=problem_id)
    solution.verdict = verdict
    solution.submitted_at = timezone.now()
    solution.submitted_code = codeText
    solution.save()

    return redirect('oj:submissions')

@login_required
def submissions(request):
    submission = Solutions.objects.all()
    context = {'submission': submission}
    return render(request, 'oj/submissions.html', context)