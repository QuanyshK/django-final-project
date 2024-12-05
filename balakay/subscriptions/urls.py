from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgeGroupViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register(r'age-groups', AgeGroupViewSet)
router.register(r'subscriptions', SubscriptionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
