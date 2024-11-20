from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncMonth
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from centers.models import Center, Booking


class AnalyticsData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = (
            User.objects.annotate(month=TruncMonth('date_joined'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        center_data = (
            Center.objects.values('city')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        booking_data = (
            Booking.objects.values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )

        analytics_data = {
            "user_registrations": {
                "months": [entry['month'].strftime("%Y-%m") for entry in user_data],
                "counts": [entry['count'] for entry in user_data],
            },
            "centers_by_city": {
                "cities": [entry['city'] for entry in center_data],
                "counts": [entry['count'] for entry in center_data],
            },
            "booking_stats": {
                "statuses": [entry['status'] for entry in booking_data],
                "counts": [entry['count'] for entry in booking_data],
            },
        }
        return Response(analytics_data)


@login_required
def analytics_view(request):
    return render(request, 'analytics/analytics.html')
