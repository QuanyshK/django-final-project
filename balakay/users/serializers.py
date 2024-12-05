from rest_framework import serializers
from .models import Client, Child, UserSubscription
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Client
        fields = '__all__'

class ChildSerializer(serializers.ModelSerializer):
    parent = ClientSerializer()

    class Meta:
        model = Child
        fields = '__all__'

class UserSubscriptionSerializer(serializers.ModelSerializer):
    parent = ClientSerializer()
    child = ChildSerializer()

    class Meta:
        model = UserSubscription
        fields = '__all__'
