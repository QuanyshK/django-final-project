from rest_framework.test import APITestCase
from rest_framework import status
from centers.models import Center

class CenterAPITestCase(APITestCase):
    def test_get_centers(self):
        response = self.client.get("/centers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_center(self):
        data = {
            "name": "Test Center",
            "manager_name": "John Doe",
            "manager_phone": "1234567890",
            "city": "Test City",
            "address": "123 Test St.",
            "description": "Test Description",
        }
        response = self.client.post("/centers/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
