from django.db import models

# Create your models here.
class Problems(models.Model):
    statement = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

class Solutions(models.Model):
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=10)
    submitted_at = models.DateTimeField('attempt date')
    submitted_code = models.TextField(default='code')

    def __str__(self) -> str:
        return self.verdict

class testCases(models.Model):
    input = models.TextField()
    output = models.TextField()
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.input