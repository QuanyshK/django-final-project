from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from subscriptions.models import AgeGroup, Subscription


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username="testuser", password="password")
        # Authenticate the client using the created user
        self.client.force_authenticate(user=self.user)
        # Create a sample AgeGroup instance
        self.age_group = AgeGroup.objects.create(age_range="4-7")

    def test_get_subscriptions(self):
        # Create a sample Subscription instance in the database for testing
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
        # Make a GET request to the /subscriptions/ endpoint
        response = self.client.get("/subscriptions/")
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

