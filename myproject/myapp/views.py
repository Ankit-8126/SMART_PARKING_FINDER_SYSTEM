from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import UserProfile


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def features(request):
    return render(request, "features.html")

def contact(request):
    return render(request, "contact.html")

def login(request):
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