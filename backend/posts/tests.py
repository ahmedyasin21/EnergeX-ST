from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class PostAPITestCase(APITestCase):
    def setUp(self):
        # Create some initial posts with user_id=1
        user = User.objects.create_user(
            username="hope",
            email="hope@gmail.com",
            password="ppoopp00"
        )
        self.post1 = Post.objects.create(title="First Post", content="Content 1", user=user)
        self.post2 = Post.objects.create(title="Second Post", content="Content 2", user=user)

        # URL references
        self.list_url = reverse("posts:posts-list")             # /v1/api/posts/
        self.detail_url = lambda pk: reverse("posts:post-detail", args=[pk])  # /v1/api/posts/<id>/

    def test_create_post(self):
        payload = {"title": "New Post", "content": "Some content", "user": 1}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])
        self.assertEqual(response.data["user"], payload["user"])

    def test_get_single_post(self):
        response = self.client.get(self.detail_url(self.post1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.post1.id)

    def test_get_single_post_not_found(self):
        response = self.client.get(self.detail_url(999))  # non-existing post
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
