from django.contrib.auth.models import User
from django.db.models.functions import TruncMonth
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from centers.models import Center, Booking


class AnalyticsData(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_data(self):
        user_queryset = User.objects.annotate(month=TruncMonth("date_joined"))
        user_data = (
            user_queryset.values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )
        return {
            "months": [entry["month"].strftime("%Y-%m") for entry in user_data],
            "counts": [entry["count"] for entry in user_data],
        }

    def get_center_data(self):
        center_data = (
            Center.objects.values("city")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        return {
            "cities": [entry["city"] for entry in center_data],
            "counts": [entry["count"] for entry in center_data],
        }

    def get_booking_data(self):
        booking_data = (
            Booking.objects.values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        )
        return {
            "statuses": [entry["status"] for entry in booking_data],
            "counts": [entry["count"] for entry in booking_data],
        }

    def get_user_activity(self):
        user_activity = (
            Booking.objects.values("user__username")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        return {
            "users": [entry["user__username"] for entry in user_activity[:5]],  # Top 5 active users
            "counts": [entry["count"] for entry in user_activity[:5]],
        }

    def get(self, request):
        analytics_data = {
            "user_registrations": self.get_user_data(),
            "centers_by_city": self.get_center_data(),
            "booking_stats": self.get_booking_data(),
            "activity_stats": self.get_user_activity(),
        }
        return Response(analytics_data)


@login_required
def analytics_view(request):
    booking_queryset = Booking.objects.all()
    user_queryset = User.objects.annotate(month=TruncMonth("date_joined"))

    user_data = (
        user_queryset.values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )
    user_registrations = {
        "months": [entry["month"].strftime("%Y-%m") for entry in user_data],
        "counts": [entry["count"] for entry in user_data],
    }

    center_data = (
        Center.objects.values("city")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    centers_by_city = {
        "cities": [entry["city"] for entry in center_data],
        "counts": [entry["count"] for entry in center_data],
    }

    booking_data = (
        booking_queryset.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )
    booking_stats = {
        "statuses": [entry["status"] for entry in booking_data],
        "counts": [entry["count"] for entry in booking_data],
    }

    user_activity = (
        Booking.objects.values("user__username")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    activity_stats = {
        "users": [entry["user__username"] for entry in user_activity[:5]],  # Top 5 active users
        "counts": [entry["count"] for entry in user_activity[:5]],
    }

    analytics_data = {
        "user_registrations": user_registrations,
        "centers_by_city": centers_by_city,
        "booking_stats": booking_stats,
        "activity_stats": activity_stats,
    }

    return render(request, "analytics/analytics.html", {"analytics_data": analytics_data})
