from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.http import HttpResponse
from django.http import FileResponse
import os, io, sys, re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Question, Answer
import pyqrcode
from django.core.exceptions import ObjectDoesNotExist

# def index(request):
#     return render(request, 'questions/index.html',)


def registration(request):
    if request.method == "POST":
        name = request.POST['name'].strip()
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # name = name.strip()
        name_regex = "^[A-Za-z0-9_-_\s]*$"
        if re.match(name_regex, name):
            if password1 == password2:
                try:
                    User.objects.get(username=name)
                    print(">>>>> User already exists")
                except ObjectDoesNotExist:
                    print(">>>>> User created\nName: "+name+"\nPasswd: "+password1)
                    user = User.objects.create_user(username=name, password=password1)
                    user.save()
                    return HttpResponseRedirect('login')

    return render(request, 'questions/registration.html',)


def qrcode(request, q_id):
    # qrdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    qrdir = 'files/qrcode/'
    qr_url = request.build_absolute_uri("/addanswer/" + str(q_id))
    url = pyqrcode.create(qr_url)
    buffer = io.BytesIO()
    url.svg(buffer, scale=10)
    qr_file = qrdir + str(q_id) + '.svg'
    with open(qr_file, 'wb') as f:
        f.write(buffer.getvalue())
        f.close()
    print("QRCODE_FUNCTION\n" + qr_file)

    str1 = "files/"
    qr_filename_db = qr_file[len(str1):]
    q_url = request.build_absolute_uri("/question/" + str(q_id))
    Question.objects.filter(id=q_id).update(qrcode=qr_filename_db, url=q_url)
    # return qr_file


def user_login(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            # def login(request) and login() def login() must have another name
            login(request, user)
            return HttpResponseRedirect(reverse('questions'))
        # else:
        #     return render(request, 'questions/error.html', )
    return render(request, 'questions/login.html',)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def questions(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login')
    else:
        if request.method == "POST":
            question = Question()
            question.owner = request.user.username
            question.text = request.POST['text']
            if question.text:
                # save to database
                # question.save()

                # get latest added object from db
                question = Question.objects.order_by('id').last()   # return Object
                print("last question id = " + str(question.id))
                # qr_url = request.build_absolute_uri("addanswer/" + str(question.id))
                qrcode(request, question.id)
            else:
                return HttpResponseRedirect(reverse('questions'))
                # return HttpResponse("<h2>Что то пошло не так=)</h2>")

        question_list = Question.objects.filter(owner=request.user.username).order_by('-date')
        return render(request, 'questions/question.html', {"question_list": question_list})


def show_question(request, q_id):
    # question = Question.objects.filter(id=id) # return QuerySet
    try:
        question = Question.objects.get(id=q_id)  # return Object
        url = question.url
        q_url = request.build_absolute_uri("/question/" + str(q_id))
        if url != q_url:
            qrcode(request, q_id)
            # return HttpResponseRedirect(url)
    except ObjectDoesNotExist:
        question = None
        print("question does not exist")

    return render(request, 'questions/show_question.html', {"question": question,})


def delete_question(request, q_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login')
    else:
        question = Question.objects.get(id=q_id)
        if question.owner == request.user.username:
            question.delete()
            Answer.objects.filter(question_id=q_id).delete()
            # Question.objects.filter(id=q_id).delete()
            # Добавить удаление qrcode
    return HttpResponseRedirect(reverse('questions'))


def add_answer(request, q_id):
    if request.method == "POST":
        answer = Answer()
        answer.owner = request.POST['name']
        answer.classname = request.POST['classname']
        answer.text = request.POST['answer']
        answer.question_id = q_id
        answer.save()
        return HttpResponse('<h2>Ответ принят!</h2>')
    question = Question.objects.filter(id=q_id)
    return render(request, 'questions/addanswer.html', {"question": question})


def show_answer(request, q_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login')
    else:
        answers = Answer.objects.filter(question_id=q_id)
        return render(request, 'questions/answers.html', {"answers": answers})


# def getfile(request, filename):
#     print("def getfile*************************")
#     response = FileResponse(open(filename, 'rb'))
#     print("FileName == " + filename)
#     return response
