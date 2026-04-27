from django.shortcuts import render

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
    return render(request, "signup.html")

def forgot(request):
    return render(request, "forgot.html")

def otp(request):
    return render(request, "otp.html")

def navbar(request):
    return render(request, "navbar.html")

def footer(request):
    return render(request, "footer.html")