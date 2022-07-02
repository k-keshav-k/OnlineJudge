from django.db import models

# Create your models here.
class Problems(models.Model):
    statement = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

class Solutions(models.Model):
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=10)
    submitted_at = models.DateTimeField('attempt date')

class testCases(models.Model):
    input = models.CharField(max_length=500)
    output = models.CharField(max_length=500)
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE)