from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_client, name='register'),
    path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('add-child/', views.add_child_view, name='add_child'),
]
