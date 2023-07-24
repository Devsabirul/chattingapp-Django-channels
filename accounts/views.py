from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

def signin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("Home")
            else:
                msg = "something is wrong!"
        return render(request, "account/login.html", locals())
    else:
        return redirect("Home")


def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            avatar = request.FILES.get('avatar')
            check_user = User.objects.filter(username=username).exists()
            if not check_user:
                user = User.objects.create_user(
                    first_name=name, email=email, username=username, password=password,avatar=avatar)
                user.save()
                return redirect('signin')
            else:
                msg = "Username already exists!"
        return render(request, "account/register.html", locals())
    else:
        return redirect('Home')


@login_required(login_url='signin')
def logout_(request):
    logout(request)
    return redirect("Home")
