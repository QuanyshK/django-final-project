from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from centers.models import Center

class CenterAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username="testuser", password="password")
        # Force authentication for the client using the created user
        self.client.force_authenticate(user=self.user)

    def test_get_centers(self):
        # Create a sample Center instance in the database for testing
        Center.objects.create(
            name="Test Center",
            manager_name="John Doe",
            manager_phone="1234567890",
            city="Test City",
            address="123 Test St.",
            description="Test Description",
        )
        # Make a GET request to the /centers/ endpoint
        response = self.client.get("/centers/")
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

