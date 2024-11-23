from rest_framework import serializers
from .models import Category, Center, Section, Schedule, Booking, FavoriteSection


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    center = serializers.StringRelatedField()  
    category = serializers.StringRelatedField() 

    class Meta:
        model = Section
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    section = serializers.StringRelatedField()  

    class Meta:
        model = Schedule
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() 
    client = serializers.StringRelatedField()  
    schedule = ScheduleSerializer()  
    child = serializers.StringRelatedField()  

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['created_at', 'confirmed_at', 'cancelled_at']

    def update(self, instance, validated_data):
        if instance.is_expired():
            raise serializers.ValidationError("Cannot update an expired booking.")
        return super().update(instance, validated_data)


class FavoriteSectionSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField() 
    section = serializers.StringRelatedField()  

    class Meta:
        model = FavoriteSection
        fields = '__all__'
        extra_kwargs = {
            'added_at': {'read_only': True},  
        }
