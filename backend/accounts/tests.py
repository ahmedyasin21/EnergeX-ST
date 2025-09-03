from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthTests(APITestCase):
    def test_register_user(self):
        payload = {
            "username": "hamza",
            "email": "hamza@gmail.com",
            "password": "ppoopp00",
            "re_password": "ppoopp00"
        }
        url = reverse("accounts:register")  # include app namespace
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User registered successfully.")

    def test_login_user(self):
        user = User.objects.create_user(
            username="hamza",
            email="hamza@gmail.com",
            password="ppoopp00"
        )
        payload = {"username": "hamza", "password": "ppoopp00"}
        url = reverse("login")
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)