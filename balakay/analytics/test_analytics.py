from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from centers.models import Center, Booking
from django.utils import timezone
from datetime import timedelta


class AnalyticsDataTests(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create a test client for making API requests
        self.client = APIClient()

        # Create some test data: users, centers, and bookings
        # Creating users with different registration dates
        self.user1 = User.objects.create_user(username='user1', password='password',
                                              date_joined=timezone.now() - timedelta(days=30))
        self.user2 = User.objects.create_user(username='user2', password='password',
                                              date_joined=timezone.now() - timedelta(days=60))

        # Create centers
        self.center1 = Center.objects.create(name="Center 1", city="City A")
        self.center2 = Center.objects.create(name="Center 2", city="City B")

        # Create bookings
        self.booking1 = Booking.objects.create(status="confirmed", user=self.user1, center=self.center1)
        self.booking2 = Booking.objects.create(status="pending", user=self.user2, center=self.center2)

    def test_get_analytics_data_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='password')

        # Send a GET request to the analytics API endpoint
        response = self.client.get(reverse('analytics_data'))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the expected structure
        data = response.json()

        # Test if user registration data is correctly returned
        self.assertIn('user_registrations', data)
        self.assertTrue(len(data['user_registrations']['months']) > 0)
        self.assertTrue(len(data['user_registrations']['counts']) > 0)

        # Test if center data is correctly returned
        self.assertIn('centers_by_city', data)
        self.assertTrue(len(data['centers_by_city']['cities']) > 0)
        self.assertTrue(len(data['centers_by_city']['counts']) > 0)

        # Test if booking data is correctly returned
        self.assertIn('booking_stats', data)
        self.assertTrue(len(data['booking_stats']['statuses']) > 0)
        self.assertTrue(len(data['booking_stats']['counts']) > 0)

    def test_get_analytics_data_unauthenticated(self):
        # Send a GET request to the analytics API without logging in
        response = self.client.get(reverse('analytics_data'))

        # Check that the response is a 403 (Forbidden) since the user is not authenticated
        self.assertEqual(response.status_code, 403)


class AnalyticsViewTests(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_analytics_view_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='password')

        # Send a GET request to the analytics dashboard view
        response = self.client.get(reverse('analytics_dashboard'))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the correct template is used
        self.assertTemplateUsed(response, 'analytics/analytics.html')

    def test_analytics_view_unauthenticated(self):
        # Send a GET request to the analytics dashboard view without logging in
        response = self.client.get(reverse('analytics_dashboard'))

        # Check that the response redirects to the login page
        self.assertRedirects(response, f'/accounts/login/?next={reverse("analytics_dashboard")}')
