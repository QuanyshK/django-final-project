from rest_framework import viewsets
from .models import AgeGroup, Subscription
from .serializers import AgeGroupSerializer, SubscriptionSerializer


class AgeGroupViewSet(viewsets.ModelViewSet):
    queryset = AgeGroup.objects.all()
    serializer_class = AgeGroupSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
