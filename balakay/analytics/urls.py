from django.urls import path
from .views import AnalyticsData, analytics_view

urlpatterns = [
    path('data/', AnalyticsData.as_view(), name='analytics_data'),
    path('dashboard/', analytics_view, name='analytics_dashboard'),
]
