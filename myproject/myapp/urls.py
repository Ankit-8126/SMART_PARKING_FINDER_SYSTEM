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
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('footer/',views.footer,name='footer'),
    path('mydashboard/',views.mydashboard,name='mydashboard'),
    path('logout/', views.logout, name='logout'),

    path('forgot/', views.forgot, name='forgot'),
    path('reset/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('nav2/',views.nav2,name='nav2'),
    path('find-parking/', views.find_parking, name='find_parking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),


]
