from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
def signup(request):
    if request.user.is_authenticated:
        return redirect("Homepage")
    if request.method=="POST":
        username = request.POST.get("username")
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confirmpass=request.POST.get("confirmpass")

        #Validations

        if User.objects.filter(username=username).exists():
            messages.error(request,"The username you entered already exists,try another one")
            return redirect("Homepage")
        if User.objects.filter(email=email).exists():
            messages.error(request,"the email you entered is already linked with another account")
            return redirect("Homepage")
        if len(username)>10:
            messages.error(request,"Username shouldnt exceed 10 charecters")
            return redirect("Homepage")
        if password != confirmpass:
            messages.error(request,"where are your eyes siree,confirm the password correctly")
            return redirect("Homepage")

        myuser=User.objects.create_user(username,email,password)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your account is succesfully created")
        return redirect("signin")
    return render(request,"Signup.html")
def signout(request):
    logout(request)
    messages.success(request,"You have succesfully logged out")
    return redirect("Homepage")
def signin(request):
    if request.user.is_authenticated:
        return redirect("Homepage")
    if request.method=="POST":
        username= request.POST.get("username")
        password= request.POST.get("password")

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"Successfully signed in")
            context={"fname":user.first_name}
            return render(request,"Homepage.html",context)
        else:
            messages.error(request,"Invalid credentials")
            return redirect("Homepage")
    return render(request,"Signin.html")
def Homepage(request):
    return render(request,"Homepage.html")

@login_required(login_url="/")
@allowed_users(['Adminn'])
def AdminOnly(request):
    current_user=request.user
    context={"fname":current_user.first_name}
    return render(request,"Homepage.html",context)