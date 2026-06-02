from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    name = models.CharField(max_length=100)

    email = models.EmailField(
        unique=True,
        null=True,
        blank=True
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class Parking(models.Model):
    name = models.CharField(max_length=100)

    address = models.CharField(max_length=200)

    price = models.PositiveIntegerField()

    available_slots = models.PositiveIntegerField(
        default=0
    )

    latitude = models.FloatField()

    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Booking(models.Model):
    PAYMENT_CHOICES = [
        ("SUCCESS", "Success"),
        ("PENDING", "Pending"),
        ("FAILED", "Failed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    parking = models.ForeignKey(
        Parking,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    booked_at = models.DateTimeField(
        auto_now_add=True
    )

    hours = models.PositiveIntegerField(
        default=1
    )

    total_price = models.PositiveIntegerField(
        default=0
    )

    start_time = models.DateTimeField(
        default=timezone.now
    )

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default="SUCCESS"
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.parking.name}"