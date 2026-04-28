from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages


# 🏠 HOME
def home(request):
    return render(request, "home.html")


# 📄 ABOUT
def about(request):
    return render(request, "about.html")


# ⚙️ FEATURES
def features(request):
    return render(request, "features.html")


# 📞 CONTACT
def contact(request):
    return render(request, "contact.html")


# 🔐 LOGIN
def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)   # ✅ FIXED
            return redirect('mydashboard')
        else:
            messages.error(request, "Invalid Email or Password")

    return render(request, "login.html")


# 📝 SIGNUP
def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

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

        # ✅ Auto login after signup
        auth_login(request, user)

        return redirect('mydashboard')

    return render(request, 'signup.html')


# 🔁 FORGOT PASSWORD (UI only)
def forgot(request):
    return render(request, "forgot.html")


# 🔢 OTP PAGE (demo)
def otp(request):
    return render(request, "otp.html")


# 🏠 DASHBOARD (Protected)
@login_required(login_url='login')
def mydashboard(request):
    return render(request, "mydashboard.html")


# 🔓 LOGOUT
def logout(request):
    auth_logout(request)
    return redirect('login')


# 📌 OPTIONAL (only if you really want separate page access)
def navbar(request):
    return render(request, "navbar.html")


def footer(request):
    return render(request, "footer.html")