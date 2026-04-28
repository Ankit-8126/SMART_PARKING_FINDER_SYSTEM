from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages
def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def features(request):
    return render(request, "features.html")

def contact(request):
    return render(request, "contact.html")

def login(request):
    if request.method=='POST':
        email=request.POST.get("email")
        password=request.POST.get("password")
        
        user=authenticate(request,username=email,password=password)
        
        if user is not None:
            auth_login
            auth_login(request,user)
            return redirect('/mydashboard/')
        else:
            messages.error(request,"Invalid Email and Password")
    
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # Check existing user
        if User.objects.filter(username=email).exists():
            return render(request, 'signup.html', {
                'error': 'Email already exists'
            })

        # Create user
        user = User.objects.create_user(
            username=email,
            first_name=name,
            email=email,
            password=password
        )
        user.save()

        return redirect('/mydashboard/')

    return render(request, 'signup.html')

def forgot(request):
    return render(request, "forgot.html")

def otp(request):
    return render(request, "otp.html")

def navbar(request):
    return render(request, "navbar.html")

def footer(request):
    return render(request, "footer.html")

def mydashboard(request):
    return render(request,"mydashboard.html")