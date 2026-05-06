from django.contrib import admin
from .models import UserProfile, Parking, Booking



# 🔹 User Profile Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'user')
    search_fields = ('name', 'email')





@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'price', 'available_slots']
    search_fields = ['name', 'address']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'parking', 'booked_at']
    list_filter = ['booked_at']
    ordering = ['-booked_at']