from django.urls import path
from . import views

urlpatterns = [
    path('',views.home ),
    path('about/',views.about),
    path('features/',views.features),
    path('contact/',views.contact),
    path('login/',views.login),
    path('navbar/',views.navbar),
    path('signup/',views.signup),
    path('forgot/',views.forgot),
    path('otp/',views.otp),
    path('footer/',views.footer),

]
