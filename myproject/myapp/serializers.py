from rest_framework import serializers
from .models import Parking, Booking

class ParkingSerializer(serializers.ModelSerializer):
    distance = serializers.FloatField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Parking
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'