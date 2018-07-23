from django.shortcuts import render, HttpResponse, redirect
from django.db import models
from .models import User, Device
from django.contrib import messages

def index(request):
    return render(request, "homepage.html")

def createUser(request):
    if request.method=="POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/', errors)
        else:
            User.objects.create(full_name=request.POST['usersName'], email_address=request.POST['usersEmail'], phone_number=request.POST['usersPhone'], device_key_name=request.POST['deviceNumber'])
            last_user = User.objects.last()
            request.session['user_id'] = last_user.id
            return redirect('/userPage')
    return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if request.POST['emailsLogin'] == 'godMode':
            return redirect('/godMode')
        elif User.objects.filter(email_address=request.POST['emailsLogin']):
            user = User.objects.get(email_address=request.POST['emailsLogin'])
            if user.device_key_name == request.POST['deviceNumber']:
                request.session['user_id'] = user.id
                return redirect('/userPage')
            elif len(errors):
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/', errors)
            return redirect('/')
    return redirect('/')

def userPage(request):
    user_id = User.objects.get(id=request.session['user_id'])
    context = {
        'name':user_id.full_name
    }
    return render(request, "eventPage.html", context)

def godModeCheck(request):
    if request.method == "POST":
        if request.POST['godModeLogin'] == "Dylan Rose" and request.POST['godModePassword'] == "isourboss":
            return redirect('/godMode')
        else:
            return redirect('/')

def godMode(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, "godMode.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def deleteUser(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('/godMode')
