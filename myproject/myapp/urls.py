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
    path(
        'mydashboard/',
        views.mydashboard,
        name='mydashboard'
    ),
    path('logout/', views.logout, name='logout'),

    path('forgot/', views.forgot, name='forgot'),
    path('reset/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('nav2/',views.nav2,name='nav2'),

    path('my-bookings/', views.my_bookings, name='my_bookings'),

    path('my-profile/', views.my_profile, name='my_profile'),

    path('settings/', views.user_settings, name='settings'),

    path('find-parking/', views.find_parking_page,name='find_parking'),
    path('api/nearby-parkings/', views.nearby_parkings,name='nearby_parkings'),
    path('api/book-parking/', views.book_parking,name='book_parking'),
    path('api/booking-history/', views.booking_history,name='booking_history'),
    path('all-parking/', views.all_parkings, name='all_parking'),

    path('parking/<int:id>/', views.parking_detail, name='parking_detail'),

   path('book-now/<int:parking_id>/', views.book_now, name='book_now'),

    path(
        'cancel-booking/<int:booking_id>/',
        views.cancel_booking,
        name='cancel_booking'
    ),


]