from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    email = models.EmailField(
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):

        return self.email if self.email else self.user.username


class Parking(models.Model):

    name = models.CharField(max_length=100)

    address = models.CharField(max_length=200)

    price = models.IntegerField()

    available_slots = models.IntegerField(default=0)

    latitude = models.FloatField()

    longitude = models.FloatField()

    def __str__(self):

        return self.name


class Booking(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    parking = models.ForeignKey(
        Parking,
        on_delete=models.CASCADE
    )

    booked_at = models.DateTimeField(
        auto_now_add=True
    )

    hours = models.IntegerField(default=1)

    total_price = models.IntegerField(default=0)

    start_time = models.DateTimeField(
        default=timezone.now
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    payment_status = models.CharField(
        max_length=20,
        default="SUCCESS"
    )

    is_active = models.BooleanField(
        default=True
    )

    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    payment_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):

        return f"{self.user.username} - {self.parking.name}"