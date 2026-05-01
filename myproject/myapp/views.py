from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator

# Email validation
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .tokens import account_activation_token


# 🏠 HOME
def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def features(request):
    return render(request, "features.html")


def contact(request):
    return render(request, "contact.html")


# 🔐 LOGIN
def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('mydashboard')
            else:
                messages.error(request, "⚠️ Please verify your email first")
        else:
            messages.error(request, "❌ Invalid Email or Password")

    return render(request, "login.html")


# 📝 SIGNUP + EMAIL VERIFY
def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # ✅ Email format validation
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'signup.html', {
                'error': '❌ Invalid email format'
            })

        # ✅ Check existing user
        if User.objects.filter(username=email).exists():
            return render(request, 'signup.html', {
                'error': '❌ Email already exists'
            })

        # ✅ Create inactive user
        user = User.objects.create_user(
            username=email,
            first_name=name,
            email=email,
            password=password
        )
        user.is_active = False
        user.save()

        # 🔥 Activation link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        link = f"http://127.0.0.1:8000/activate/{uid}/{token}/"

        # 📧 Send email
        try:
            send_mail(
                'Activate your account',
                f'Hi {name},\n\nClick this link to activate your account:\n{link}',
                'ankitparmar8126@gmail.com',
                [email],
                fail_silently=False
            )
        except Exception:
            return render(request, 'signup.html', {
                'error': '❌ Email sending failed (check App Password)'
            })

        return render(request, 'signup.html', {
            'message': '✅ Check your email to activate your account'
        })

    return render(request, 'signup.html')


# 🔗 ACTIVATE ACCOUNT
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "✅ Account activated successfully. Login now.")
        return redirect('login')
    else:
        return HttpResponse("❌ Invalid or expired activation link")


# 🔁 FORGOT PASSWORD (SEND RESET LINK)
def forgot(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            return render(request, "forgot.html", {
                "error": "❌ Email not found"
            })

        # 🔥 Reset link generate
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        link = f"http://127.0.0.1:8000/reset/{uid}/{token}/"

        # 📧 Send email
        try:
            send_mail(
                'Reset your password',
                f'Click this link to reset your password:\n{link}',
                'ankitparmar8126@gmail.com',
                [email],
                fail_silently=False
            )
        except Exception:
            return render(request, "forgot.html", {
                "error": "❌ Email sending failed"
            })

        return render(request, "forgot.html", {
            "message": "✅ Reset link sent to your email"
        })

    return render(request, "forgot.html")


# 🔑 RESET PASSWORD
def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):

        if request.method == "POST":
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()

            messages.success(request, "✅ Password reset successful. Login now.")
            return redirect('login')

        return render(request, 'reset.html')

    else:
        return HttpResponse("❌ Invalid or expired reset link")


# 🏠 DASHBOARD
@login_required(login_url='login')
def mydashboard(request):
    return render(request, "mydashboard.html")


# 🔓 LOGOUT
def logout(request):
    auth_logout(request)
    return redirect('login')


# OPTIONAL
def navbar(request):
    return render(request, "navbar.html")


def footer(request):
    return render(request, "footer.html")
def nav2(request):
    return render(request, "nav2.html")

def find_parking(request):
    return render(request, "find_parking.html")

def my_bookings(request):
    return render(request, "my_bookings.html")