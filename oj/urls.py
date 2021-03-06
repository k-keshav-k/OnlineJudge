from django.urls import path

from . import views

app_name='oj'
urlpatterns = [
    path('', views.problems, name = "problems"),
    path('problem/<int:problem_id>', views.problemDetail, name='problem_detail'),
    path('problem/<int:problem_id>/submit', views.submitCode, name="submit"),
    path('submissions', views.submissions, name="submissions"),
]
