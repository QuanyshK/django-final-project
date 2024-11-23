from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from subscriptions.models import AgeGroup, Subscription


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.age_group = AgeGroup.objects.create(age_range="4-7")

    def test_get_subscriptions(self):
        Subscription.objects.create(
            name="Test Subscription",
            price=100.0,
            duration_text="1 month",
            age_group=self.age_group,
            total_days=30,
            freeze_days=5,
            daily_visits=3,
            monthly_visits=20,
            premium_monthly_visits=5,
        )
        response = self.client.get("/subscriptions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

