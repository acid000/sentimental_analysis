from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
# Create your views here.
@csrf_protect
def Signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            print("username already occured")
            return redirect('/')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            print("email already occured")
            return redirect('/')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            print("user<20")
            return redirect('/')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            print("password didn't match")
            return redirect('/')
        
       
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        return redirect('/add_review')
        
        
    return render(request, "signup.html")

@csrf_protect
def Signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Sucessfully!!")
            return redirect('/add_review')
        else:
            messages.error(request, "Bad Credentials!!")
            print("bad credential")
            return redirect('/')
    
    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('/')
