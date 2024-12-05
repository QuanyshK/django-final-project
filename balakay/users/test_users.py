from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from users.models import Client, Child, UserSubscription
from subscriptions.models import Subscription


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.client_profile = Client.objects.create(
            user=self.user,
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            city="Test City",
        )
        self.subscription = Subscription.objects.create(
            name="Basic Plan",
            price=100,
            duration_text="30 days",
            total_days=30,
            freeze_days=10,
            daily_visits=3,
            monthly_visits=30,
            premium_monthly_visits=5,
        )
        self.child = Child.objects.create(
            parent=self.client_profile,
            first_name="Child",
            last_name="One",
            birth_date="2015-01-01",
            gender="male",
        )
        self.user_subscription = UserSubscription.objects.create(
            parent=self.client_profile,
            child=self.child,
            subscription_type=self.subscription,
            total_days=30,
            freeze_days=10,
            daily_visits_limit=2,
            total_visits=20,
        )

    def test_register_client(self):
        self.client.logout()
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "first_name": "New",
            "last_name": "Client",
            "phone_number": "9876543210",
            "city": "New City",
        }
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertTrue(Client.objects.filter(phone_number="9876543210").exists())

    def test_login(self):
        self.client.logout()
        data = {
            "username": "testuser",
            "password": "password",
        }
        response = self.client.post('/users/', data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_logout(self):
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_get_profile(self):
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.client_profile.first_name)

    def test_subscription_detail(self):
        response = self.client.get(f'/users/subscription_detail/{self.user_subscription.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user_subscription.is_active)
