from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from users.models import Client, Child


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.client_profile = Client.objects.create(
            user=self.user,
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            city="Test City",
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
        response = self.client.post('/users/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username="newuser").count(), 1)

    def test_get_profile(self):
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.client_profile.first_name)

    def test_update_profile(self):
        data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "first_name": "Updated",
            "last_name": "User",
            "phone_number": "1234567891",
            "city": "Updated City",
        }
        response = self.client.patch('/users/profile/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client_profile.refresh_from_db()
        self.assertEqual(self.client_profile.first_name, "Updated")
        self.assertEqual(self.client_profile.city, "Updated City")
        self.assertEqual(self.user.username, "updateduser")

    def test_add_child(self):
        data = {
            "first_name": "Child",
            "last_name": "One",
            "birth_date": "2018-01-01",
            "gender": "male",
        }
        response = self.client.post('/users/add-child/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        child = Child.objects.get(first_name="Child")
        self.assertEqual(child.gender, "male")
        self.assertEqual(child.birth_date.strftime("%Y-%m-%d"), "2018-01-01")
