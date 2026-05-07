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
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .tokens import account_activation_token
from .models import Parking, Booking
from .utils import haversine

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str

# ================= Authentication =================

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

        # ✅ Validate email
        try:
            validate_email(email)

        except ValidationError:
            return render(request, 'signup.html', {
                'error': '❌ Invalid email format'
            })

        # ✅ Check existing email
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

        # ✅ Generate token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        # ✅ Dynamic domain
        current_site = get_current_site(request)

        activation_link = (
            f"https://{current_site.domain}"
            f"/activate/{uid}/{token}/"
        )

        # ✅ Send email
        try:

            send_mail(
                subject='Activate your Smart Parking account',

                message=f'''
Hi {name},

Click below link to activate your account:

{activation_link}

If you did not create this account, ignore this email.
''',

                from_email='ankitparmar8126@gmail.com',
                recipient_list=[email],
                fail_silently=False
            )

            return render(request, 'signup.html', {
                'message': '✅ Verification link sent to your email'
            })

        except Exception as e:

            return render(request, 'signup.html', {
                'error': f'❌ Email sending failed: {str(e)}'
            })

    return render(request, 'signup.html')


# 🔗 ACTIVATE ACCOUNT
def activate(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):

        user.is_active = True
        user.save()

        messages.success(
            request,
            "✅ Account activated successfully. Login now."
        )

        return redirect('login')

    else:
        return HttpResponse("❌ Invalid or expired activation link")


# 🔁 FORGOT PASSWORD
def forgot(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:
            user = User.objects.get(username=email)

        except User.DoesNotExist:

            return render(request, "forgot.html", {
                "error": "❌ Email not found"
            })

        # ✅ Generate token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # ✅ Dynamic domain
        current_site = get_current_site(request)

        reset_link = (
            f"https://{current_site.domain}"
            f"/reset/{uid}/{token}/"
        )

        # ✅ Send email
        try:

            send_mail(
                subject='Reset Your Password',

                message=f'''
Click below link to reset your password:

{reset_link}

If you did not request this, ignore this email.
''',

                from_email='ankitparmar8126@gmail.com',
                recipient_list=[email],
                fail_silently=False
            )

            return render(request, "forgot.html", {
                "message": "✅ Reset link sent to your email"
            })

        except Exception as e:

            return render(request, "forgot.html", {
                "error": f"❌ Email sending failed: {str(e)}"
            })

    return render(request, "forgot.html")


# 🔑 RESET PASSWORD
def reset_password(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):

        if request.method == "POST":

            new_password = request.POST.get('password')

            user.set_password(new_password)
            user.save()

            messages.success(
                request,
                "✅ Password reset successful. Login now."
            )

            return redirect('login')

        return render(request, 'reset.html')

    else:
        return HttpResponse("❌ Invalid or expired reset link")



# ================= BASIC PAGES =================

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def features(request):
    return render(request, "features.html")

def contact(request):
    return render(request, "contact.html")


# ================= LOGIN =================


# ================= DASHBOARD =================

@login_required(login_url='login')
def mydashboard(request):
    return render(request, "mydashboard.html")


# ================= LOGOUT =================

def logout(request):
    auth_logout(request)
    return redirect('login')


# ================= FIND PARKING (FIXED) =================

from .utils import haversine

@login_required(login_url='login')
def find_parking_page(request):

    user_lat = request.POST.get("latitude")
    user_lng = request.POST.get("longitude")

    parkings = Parking.objects.all()

    data = []

    for p in parkings:

        distance = None

        # ✅ only calculate if user location exists
        if user_lat and user_lng:
            try:
                distance = haversine(
                    float(user_lat),
                    float(user_lng),
                    p.latitude,
                    p.longitude
                )
            except:
                distance = None

        data.append({
            "id": p.id,
            "name": p.name,
            "address": p.address,
            "price": p.price,
            "available_slots": p.available_slots,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "distance": round(distance, 2) if distance else None
        })

    return render(request, "find_parking.html", {"parkings": data})

# ================= PROFILE =================

@login_required(login_url='login')
def my_profile(request):
    return render(request, "my_profile.html")


# ================= SETTINGS =================

@login_required(login_url='login')
def settings(request):
    return render(request, "settings.html")


# ================= NAV =================

def navbar(request):
    return render(request, "navbar.html")

def footer(request):
    return render(request, "footer.html")

def nav2(request):
    return render(request, "nav2.html")


# ================= NEARBY PARKINGS API =================

@api_view(['POST'])
def nearby_parkings(request):
    try:
        user_lat = float(request.data.get("lat") or 0)
        user_lng = float(request.data.get("lng") or 0)
    except:
        return Response({"error": "Invalid coordinates"}, status=400)

    parkings = Parking.objects.all()
    results = []

    for p in parkings:
        distance = haversine(user_lat, user_lng, p.latitude, p.longitude)

        results.append({
            "id": p.id,
            "name": p.name,
            "address": p.address,
            "available_slots": p.available_slots,
            "price": p.price,
            "distance": round(distance, 2),
            "status": "Available" if p.available_slots > 0 else "Full"
        })

    results.sort(key=lambda x: x["distance"])

    return Response({"parkings": results})


# ================= BOOK PARKING =================

@api_view(['POST'])
def book_parking(request):
    parking_id = request.data.get("parking_id")

    try:
        with transaction.atomic():
            parking = Parking.objects.select_for_update().get(id=parking_id)

            if parking.available_slots <= 0:
                return Response({"error": "Parking Full"}, status=400)

            parking.available_slots -= 1
            parking.save()

            Booking.objects.create(
                parking=parking,
                user=request.user
            )

        return Response({"message": "Booking Confirmed"})

    except Parking.DoesNotExist:
        return Response({"error": "Parking not found"}, status=404)


# ================= BOOKING HISTORY =================

@api_view(['GET'])
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')

    data = []
    for b in bookings:
        data.append({
            "parking": b.parking.name,
            "user": b.user.username,
            "time": b.booked_at.strftime("%Y-%m-%d %H:%M")
        })

    return Response({"bookings": data})

def all_parkings(request):
    parkings = Parking.objects.all()

    user_lat = request.GET.get("lat")
    user_lng = request.GET.get("lng")

    if user_lat and user_lng:
        user_lat = float(user_lat)
        user_lng = float(user_lng)

        for p in parkings:
            p.distance = haversine(user_lat, user_lng, p.latitude, p.longitude)
    else:
        for p in parkings:
            p.distance = None

    return render(request, "all_parkings.html", {"parkings": parkings})

from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required(login_url='login')
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, "my_bookings.html", {"bookings": bookings})

from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def parking_detail(request, id):
    parking = get_object_or_404(Parking, id=id)
    return render(request, "parking_details.html", {"p": parking})