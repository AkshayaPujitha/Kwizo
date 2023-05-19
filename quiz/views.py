from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth,User
from django.db.models import Q
from django.contrib import messages
from .models import *
from django.urls import reverse


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
        print(quiz_id)
        quiz_id=int(quiz_id)
        quizs=Quiz.objects.filter()
        for quiz in quizs:
            print(quiz.quiz_id)
            if quiz_id==quiz.quiz_id:
                flag=1
        
        if flag==1:
            if request.user.is_authenticated:
                current_user = request.user

                student =Student.objects.filter()
                for s in student:
                    print(s.user,current_user,s.quiz)
                    if current_user==s.user and quiz_id==(s.quiz).quiz_id:
                        return render(request,'already_given.html')


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
        quiz_id
    return render(request,"score.html",ctx)


def teacher(request):
    if request.method=="POST":
        quiz_title=request.POST['quiz_title']
        num_questions=request.POST['num_questions']
        print(quiz_title,num_questions)
        ctx={'num_questions':num_questions}
        return render(request,'add_question.html',ctx)
    
    return render(request,'teacher.html')

def leader(request):
    return render(request,'leader_board.html')

def logout(request):
    auth.logout(request)
    return render(request,"home.html")

#teacher section

def createquestions(request):
        q_id = request.GET.get('data')
        quiz = Quiz.objects.filter(quiz_id=q_id).first()
        print(q_id)
    # print(quiz.quiz_title)
    # for i in quiz.num_questions:
        if request.method == 'POST':
            question_text = request.POST['question']
            option1_text = request.POST['option1']
            option2_text = request.POST['option2']
            option3_text = request.POST['option3']
            option4_text = request.POST['option4']
            quiz_id = request.POST.get('quiz_id')
            correct_option_value = request.POST['correct_option']
            quiz = Quiz.objects.filter(quiz_id=quiz_id).first()
            # Create the new question object
            new_question = Question.objects.create(
                quiz=quiz,
                questin_text=question_text,
                    )
            new_question.save()
            # Create the choice objects
            choices = [
                Choice(
                    question=new_question,
                    choice_text=option1_text,
                    correct=(correct_option_value == 'option1')
                ),
                Choice(
                    question=new_question,
                    choice_text=option2_text,
                    correct=(correct_option_value == 'option2')
                ),
                Choice(
                    question=new_question,
                    choice_text=option3_text,
                    correct=(correct_option_value == 'option3')
                ),
                Choice(
                    question=new_question,
                    choice_text=option4_text,
                    correct=(correct_option_value == 'option4')
                )
            ]
            Choice.objects.bulk_create(choices)
            context = {
                'quiz':quiz
            }
            return render(request,'createquestion.html',context)
        
        return render(request, 'createquestion.html', {'quiz': quiz})

q_id=[]
def createquiz(request):
    global q_id
    if request.method=="POST":
        quiz_title=request.POST['quiz_title']
        quiz_id=request.POST['quiz_id']
        num_questions=request.POST['num_questions']
        if Quiz.objects.filter(quiz_id=quiz_id).exists():
            reverse_url = reverse('createquestions')+f'?data={quiz_id}'
            return HttpResponseRedirect(reverse_url)
        else:
            quiz = Quiz.objects.create(quiz_title=quiz_title,quiz_id=quiz_id,num_questions=num_questions)
            quiz.save()
            context={'user':None}
            print("User Saved")
            ctx={'quiz_title':quiz_title,
                 'quiz_id':quiz_id,
                'num_questions':num_questions}
            q_id.append(quiz_id)
            return render(request,'createquestion.html',ctx)
    
    return render(request,'quizcreate.html')

def quiz_t(request):
    if request.method=="POST":
        quiz_title=request.POST['quiz_title']
        quiz_id=request.POST['quiz_id']
        num_questions=request.POST['num_questions']
        ctx={'quiz_title':quiz_title,
             'quiz_id':quiz_id,
             'num_questions':num_questions}
        return render(request,'createquestion.html',ctx)
    
    return render(request,'quizcreate.html')

def editquestion(request,id):
    question = get_object_or_404(Question,id=id)
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        choice1_text = request.POST.get('choice1_text')
        choice2_text = request.POST.get('choice2_text')
        choice3_text = request.POST.get('choice3_text')
        choice4_text = request.POST.get('choice4_text')
        correct_choice = request.POST.get('correct_choice')

        question.question_text = question_text
        question.choice_set.all().delete()

        choice1 = Choice(
            question=question,
            choice_text=choice1_text,
            correct=(correct_choice == 'choice1')
        )
        choice1.save()

        choice2 = Choice(
            question=question,
            choice_text=choice2_text,
            correct=(correct_choice == 'choice2')
        )
        choice2.save()

        choice3 = Choice(
            question=question,
            choice_text=choice3_text,
            correct=(correct_choice == 'choice3')
        )
        choice3.save()

        choice4 = Choice(
            question=question,
            choice_text=choice4_text,
            correct=(correct_choice == 'choice4')
        )
        choice4.save()

        return redirect('quiz', quiz_id=question.quiz.id)

    context = {
        'question': question
    }
    
    return render(request, 'editdata.html', context)

def add(request):
    return HttpResponse("hello")



def process_form(request):
    global q_id
    if request.method == 'POST':
        if 'add' in request.POST:
            m=len(q_id)
            print("hi",q_id)
            quiz = Quiz.objects.filter(quiz_id=int(q_id[m-1])).first()
            print("hi",q_id)
    # print(quiz.quiz_title)
    # for i in quiz.num_questions:
            question_text = request.POST['question']
            option1_text = request.POST['option1']
            option2_text = request.POST['option2']
            option3_text = request.POST['option3']
            option4_text = request.POST['option4']
            quiz_id = request.POST.get('quiz_id')
            correct_option_value = request.POST['correct_option']
            
            # Create the new question object
            new_question = Question.objects.create(
                quiz=quiz,
                questin_text=question_text,
                    )
            new_question.save()
            # Create the choice objects
            choices = [
                Choice(
                    question=new_question,
                    choice_text=option1_text,
                    correct=(correct_option_value == 'option1')
                ),
                Choice(
                    question=new_question,
                    choice_text=option2_text,
                    correct=(correct_option_value == 'option2')
                ),
                Choice(
                    question=new_question,
                    choice_text=option3_text,
                    correct=(correct_option_value == 'option3')
                ),
                Choice(
                    question=new_question,
                    choice_text=option4_text,
                    correct=(correct_option_value == 'option4')
                )
            ]
            Choice.objects.bulk_create(choices)
            context = {
                'quiz':quiz
            }
            return render(request,'createquestion.html')
        
        elif 'submit' in request.POST:
            m=len(q_id)
            #q_id = request.GET.get('data')
            quiz = Quiz.objects.filter(quiz_id=int(q_id[m-1])).first()
            print(q_id)
    # print(quiz.quiz_title)
    # for i in quiz.num_questions:
        
            question_text = request.POST['question']
            option1_text = request.POST['option1']
            option2_text = request.POST['option2']
            option3_text = request.POST['option3']
            option4_text = request.POST['option4']
            quiz_id = request.POST.get('quiz_id')
            correct_option_value = request.POST['correct_option']
            # Create the new question object
            new_question = Question.objects.create(
                quiz=quiz,
                questin_text=question_text,
                    )
            new_question.save()
            # Create the choice objects
            choices = [
                Choice(
                    question=new_question,
                    choice_text=option1_text,
                    correct=(correct_option_value == 'option1')
                ),
                Choice(
                    question=new_question,
                    choice_text=option2_text,
                    correct=(correct_option_value == 'option2')
                ),
                Choice(
                    question=new_question,
                    choice_text=option3_text,
                    correct=(correct_option_value == 'option3')
                ),
                Choice(
                    question=new_question,
                    choice_text=option4_text,
                    correct=(correct_option_value == 'option4')
                )
            ]
            Choice.objects.bulk_create(choices)
            context = {
                'quiz':quiz
            }
            return redirect('/')
    else:
        # Display the form
        return render(request, 'createquestion.html')
    
def index(request):
    return render(request,'teacher_home.html')

def delete(request):
    if request.method == 'POST':
        quiz_id=request.POST.get('quiz_id')
        quiz_id=int(quiz_id)
        q_text=request.POST.get('question')
        print(quiz_id)
        print(q_text)
        question = Question.objects.filter(quiz_id=quiz_id,questin_text=q_text)
        
        if question is None:
            pass
        else:
            print(question)
            question.delete()
            print("Deleted sucessfully")
        return render(request,'teacher_home.html')

    return render(request,'delete.html')