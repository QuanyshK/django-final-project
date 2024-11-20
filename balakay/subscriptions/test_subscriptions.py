from rest_framework.test import APITestCase
from rest_framework import status
from subscriptions.models import AgeGroup

class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.age_group = AgeGroup.objects.create(age_range="4-7")

    def test_get_subscriptions(self):
        response = self.client.get("/subscriptions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_subscription(self):
        data = {
            "active": True,
            "name": "New Subscription",
            "price": 200.0,
            "duration_text": "2 months",
            "age_group": self.age_group.id,
            "total_days": 60,
            "freeze_days": 10,
            "daily_visits": 3,
            "monthly_visits": 40,
            "premium_monthly_visits": 10,
        }
        response = self.client.post("/subscriptions/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
