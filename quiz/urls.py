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
    path('teacher.html',views.teacher,name="teacher"),
    path('leader_board.html',views.leader,name="leader"),
    path('editquestion/<int:id>',views.editquestion,name="editquestion"),
    path('createquiz',views.createquiz,name='createquiz'),
    #path('quizquestions/<int:pk>',views.showquestions,name='createquiz'),
    path('createquestions', views.createquestions, name='createquestions'),
    path('quiz',views.quiz_t,name='createquiz'),
    path('teacher.html',views.teacher,name="teacher"),
    path('add/', views.add, name='myview'),
    path('form/', views.process_form, name='process_form'),
    path('teacher_home.html',views.index,name="index"),
    path('delete.html',views.delete,name="delete"),
]
