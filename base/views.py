from datetime import datetime
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Blog

def signup(request):
    if (request.method == "POST"):
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("confirm_password")

        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists. Please choose a different username.")

        if pass1!=pass2:
            return HttpResponse("Password and confirm password doesn't match")
        
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')

    return render(request , 'signup.html')

def login(request):
    if (request.method == "POST"):
        uname = request.POST.get("username")
        passw = request.POST.get("password")

        user = authenticate(request,username=uname,password=passw)

        if (user is not None):
            auth_login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Username or password incorrect")

    return render(request , 'login.html')

@login_required(login_url='login')
def home(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'blogs': blogs , 'uname': request.user.username})

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='login')
def compose(request):
    if (request.method == "POST"):
        title = request.POST.get("title")
        content = request.POST.get("content")
        uname = request.user.username
        current_datetime = datetime.now()

        Blog.objects.create(title=title, content=content, author=uname, created_at=current_datetime)
        return redirect('home')

    return render(request, 'compose.html', {'uname': request.user.username})