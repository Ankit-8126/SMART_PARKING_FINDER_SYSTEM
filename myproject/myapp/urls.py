from django.urls import path
from . import views

urlpatterns = [
    path('',views.home ,name='home'),
    path('about/',views.about,name='about'),
    path('features/',views.features,name='features'),
    path('contact/',views.contact,name='contact'),
    path('login/',views.login,name='login'),
    path('navbar/',views.navbar,name='navbar'),
    path('signup/',views.signup,name='signup'),
    path('forgot/',views.forgot,name='forgot'),
    path('otp/',views.otp,name='otp'),
    path('footer/',views.footer,name='footer'),
    path('mydashboard/',views.mydashboard,name='mydashboard'),
    path('logout/', views.logout, name='logout')

]
