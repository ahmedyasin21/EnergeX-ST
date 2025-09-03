from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'accounts'

urlpatterns = [
    path("api/register/", views.CreateUserAPIView.as_view(),name="register")
]
