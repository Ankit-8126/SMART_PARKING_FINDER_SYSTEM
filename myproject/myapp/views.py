from django.shortcuts import render
from django.http import request,response,HttpResponse

def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")

def features(request):
    return render(request,"features.html")

def contact(request):
    return render(request,"contact.html")

def login(request):
    return render(request,"login.html")
def navbar(request):
    return render(request,"navbar.html")