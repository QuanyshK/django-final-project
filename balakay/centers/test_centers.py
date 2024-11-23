from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from centers.models import Center

class CenterAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)

    def test_get_centers(self):
        Center.objects.create(
            name="Test Center",
            manager_name="John Doe",
            manager_phone="1234567890",
            city="Test City",
            address="123 Test St.",
            description="Test Description",
        )
        response = self.client.get("/centers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

