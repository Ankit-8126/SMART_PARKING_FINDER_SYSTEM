from django.contrib import admin
from .models import UserProfile, Parking, Booking


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        queryset.delete()


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):

    def delete_model(self, request, obj):
        # delete related bookings first
        Booking.objects.filter(parking=obj).delete()
        obj.delete()

    def delete_queryset(self, request, queryset):
        Booking.objects.filter(parking__in=queryset).delete()
        queryset.delete()


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass