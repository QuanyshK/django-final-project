from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    login_view, logout_view, register_client, profile_view, update_profile, 
    add_child_view, subscription_detail, user_notifications, ClientViewSet, ChildViewSet, UserSubscriptionViewSet, 
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'children', ChildViewSet)
router.register(r'user-subscriptions', UserSubscriptionViewSet)

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_client, name='register'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('add-child/', add_child_view, name='add_child'),
    path('subscription_detail/<int:id>/', subscription_detail, name='subscription_detail'),
    path('notifications/', user_notifications, name='user_notifications'),
    path('api/', include(router.urls)),
]
