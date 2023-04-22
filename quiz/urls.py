from django.urls import path,include
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns=[
    path('',views.home,name="home"),
    path('login.html',views.login,name="login"),
    path('register.html',views.register,name="register"),
    path('logout', views.logout, name='logout'),
    path('question.html',views.question,name="question"),
    path('score',views.score,name="score"),
    path('quiz.html',views.quiz,name="quiz"),
    path('teacher.html',views.teacher,name="teacher")
]