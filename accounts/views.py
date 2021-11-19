from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


# Create your views here.
def register(request):
    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        uname = request.POST['username']
        email = request.POST['email']
        pw1 = request.POST['password1']
        pw2 = request.POST['password2']
        if pw1 != pw2:
            messages.info(request, 'Passwords did not match')
            return redirect('register')
        else:
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'Username already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=uname, password=pw1, email=email, first_name=fname, last_name=lname)
                user.save()
                return redirect('/')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pwd = request.POST['psw']
        user = authenticate(request, username=uname, password=pwd)
        if user is not None:
            print(user)
            auth_login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    return redirect('/')
