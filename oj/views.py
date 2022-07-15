from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
import os
from .models import Problems, Solutions, testCases
import tempfile
from django.contrib.auth.decorators import login_required
import subprocess

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
    lang = request.POST.get('language')
    tempSolutioncpp = tempfile.NamedTemporaryFile(suffix=".cpp", dir='.')
    tempSolutionpy = tempfile.NamedTemporaryFile(suffix=".py", dir='.')

    if (lang == "cpp"):
        tempSolutioncpp.write(str.encode(codeText))
        tempSolutioncpp.seek(0)
        tempSolutionpy.close()
    elif (lang == "python"):
        tempSolutionpy.write(str.encode(codeText))
        tempSolutionpy.seek(0)
        tempSolutioncpp.close()

    problem = get_object_or_404(Problems, pk=problem_id)

    inp = problem.testcases_set.all()

    s = subprocess.check_output('docker ps', shell=True)
    if (lang == "cpp"):
        if s.find(str.encode('gcc')) == -1:
            subprocess.run('docker run -d -it --name gcc -v /Users/keshavkrishna/Documents/django_pro/OnlineJudge:/home/:ro gcc', shell=True)
    if (lang == "python"):
        if s.find(str.encode('python')) == -1:
            subprocess.run('docker run -d -it --name python -v /Users/keshavkrishna/Documents/django_pro/OnlineJudge:/home/:ro python', shell=True)       

    if (lang == "cpp"):
        subprocess.run('docker exec gcc g++ /home/'+ os.path.basename(tempSolutioncpp.name), shell=True)

    for i in inp:
        tempOutput = tempfile.NamedTemporaryFile(suffix=".txt", dir='.')
        tempOutput.seek(0)

        tempInput = tempfile.NamedTemporaryFile(suffix=".txt", dir='.')
        tempInput.write(str.encode(i.input))

        tempInput.seek(0)
        if (lang == "cpp"):
            subprocess.run('docker exec -i gcc ./a.out < ' + tempInput.name + ' > ' + tempOutput.name, shell=True)

        elif (lang == "python"):
            subprocess.run("docker exec -i python python /home/"+ os.path.basename(tempSolutionpy.name)+ ' < '+ tempInput.name + ' > ' + tempOutput.name, shell=True)
        
        tempActualOutput = tempfile.NamedTemporaryFile(suffix=".txt", dir='.')
        tempActualOutput.write(str.encode(i.output))

        tempOutput.seek(0)
        tempActualOutput.seek(0)

        tempOutputStr = tempOutput.read().decode("utf-8")
        tempActualOutputStr = ""
        count = 0
        with open(tempActualOutput.name, 'r') as var:
            for line in var:
                count = count+1
                line = line.replace('\r', '')
                tempActualOutputStr = tempActualOutputStr + line
        
        print(tempActualOutputStr)
        print(tempOutputStr)

        if(tempActualOutputStr.strip() == tempOutputStr.strip()):
            verdict = 'Accepted'
        else:
            verdict = 'Wrong Answer'
            break

        tempOutput.close()
        tempActualOutput.close()
        tempInput.close()
    
    if (lang == "cpp"):
        tempSolutioncpp.close()
    elif (lang == "python"):
        tempSolutionpy.close()

    solution = Solutions()
    solution.problem = Problems.objects.get(pk=problem_id)
    solution.verdict = verdict
    solution.submitted_at = timezone.now()
    solution.submitted_code = codeText
    solution.save()

    return redirect('oj:submissions')

@login_required
def submissions(request):
    submission = Solutions.objects.all().order_by('-submitted_at')
    context = {'submission': submission}
    return render(request, 'oj/submissions.html', context)