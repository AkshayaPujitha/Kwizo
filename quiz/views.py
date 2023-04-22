from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth,User
from django.db.models import Q
from django.contrib import messages
from .models import *


def home(request):
    context={'user':None}
    return render(request,'home.html',context)

def register(request):
    if request.method=="POST":
        your_name=request.POST['yname']
        email=request.POST['email']    
        password=request.POST['pwd']
        cpwd=request.POST['cpwd']
        if password==cpwd:
            if User.objects.filter(username=your_name).exists():
                print('User Name Taken')
            elif User.objects.filter(email=email).exists():
                print('Email Already Taken')
            else:
                user = User.objects.create_user(username=your_name,password=password,email=email)
                user.save()
                context={'user':None}
                print("User Saved")
                return render(request,'home.html',context)
    # users=User.objects.all()
        else:
            print('Passsword Not Matching')
            return render(request,'register.html')

    return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        user=auth.authenticate(username=uname,password=pwd)
        if user is not None:
            auth.login(request,user)
            context={'user':user}
            #print(user)
            user=User.objects.filter(username=uname).first()
            return render(request,'home.html',context)
        else:
            messages.error(request,"Username or password is wrong")
    return render(request,'login.html')

quiz_id=0
#for quiz id
def quiz(request):
    global quiz_id
    flag=0
    if request.method=="POST":
        quiz_id=request.POST['quiz_id']
        quiz_id=int(quiz_id)
        quizs=Quiz.objects.filter()
        for quiz in quizs:
            if quiz_id==quiz.id:
                flag=1
        
        if flag==1:
            if request.user.is_authenticated:
                current_user = request.user

                student =Student.objects.filter()
                for s in student:
                    print(s.user,current_user,s.quiz)
                    if current_user==s.user and quiz_id==(s.quiz).id:
                        return HttpResponse("You already gave test")


                questions=Question.objects.filter()
                choices=Choice.objects.filter()
                context={'question':questions,'choices':choices,'quiz_id':quiz_id}
            return render(request,'question.html',context)
    
    return render(request,'quiz.html')

#To display the Questions and choices for the students
def question(request):
    global quiz_id
    print(quiz_id)
    if request.user.is_authenticated:
        current_user = request.user

        student =Student.objects.filter()
        for s in student:
            print(s.user,current_user,s.quiz)
            if current_user==s.user and quiz_id==(s.quiz).id:
                return HttpResponse("You already gave test")


    questions=Question.objects.filter()
    choices=Choice.objects.filter()
    context={'question':questions,'choices':choices,'quiz_id':quiz_id}
    return render(request,'question.html',context)


#dic of choices chosen by the user
user_choices = {}

#To get the score of the student
def score(request):
    global quiz_id
    marks=0
    questions=Question.objects.filter()
    for question in questions:
        choice_id = request.POST.get(f'question{question.id}')
        if choice_id:
            user_choices[question.id]=Choice.objects.get(id=choice_id)
        else:
            user_choices[question.id]=None
    print(user_choices)
    for id,obj in user_choices.items():
        #if question is unattempted by the student
        if obj is None:
            continue
        if obj.correct:
            print("Correct u scored 4 marks")
            marks+=4
        else:
            print("its incorrect")
    print(marks)
    ctx={'marks':marks}
    if request.user.is_authenticated:
        # Get the current user
        current_user = request.user
        quiz = Quiz.objects.get(id=quiz_id)
        student = Student(user=current_user, total_marks=marks, quiz=quiz)
        # Save the new Student instance to the database
        student.save()
    return render(request,"score.html",ctx)


def teacher(request):
    if request.method=="POST":
        quiz_title=request.POST['quiz_title']
        num_questions=request.POST['num_questions']
        print(quiz_title,num_questions)
        ctx={'num_questions':num_questions}
        return render(request,'add_question.html',ctx)
    
    return render(request,'teacher.html')

def logout(request):
    auth.logout(request)
    return render(request,"home.html")