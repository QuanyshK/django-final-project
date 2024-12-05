from rest_framework import serializers
from .models import AgeGroup, Subscription


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    age_group = AgeGroupSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'
