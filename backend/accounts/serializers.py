from djoser.serializers import UserCreateSerializer 
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateAccountsSerializer(UserCreateSerializer):
    """
    Serializer for user account creation, ensuring password confirmation.
    """
    re_password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Confirm your password",
        style={'input_type': 'password', 'placeholder': 'Confirm Password'}
    )

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "re_password")

    def validate(self, data):
        """
        Validate that password and re_password match.
        """
        if data.get('password') != data.get('re_password'):
            raise serializers.ValidationError({"message": "Passwords do not match"})
        return data


class StaffCreationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new staff users, ensuring password confirmation.
    """
    re_password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Confirm your password",
        style={'input_type': 'password', 'placeholder': 'Confirm Password'}
    )

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "middle_name", "last_name", "password", "re_password")

    def validate(self, data):
        """
        Validate that password and re_password match.
        """
        if data.get('password') != data.get('re_password'):
            raise serializers.ValidationError({"message": "Passwords do not match"})
        return data


class ChangePasswordRequestSerializer(serializers.Serializer):
    """
    Serializer for changing user passwords.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'New Password'}
    )
    re_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Confirm New Password'}
    )

    def validate(self, data):
        """
        Validate that password and re_password match.
        """
        if data.get('password') != data.get('re_password'):
            raise serializers.ValidationError({"message": "Passwords do not match"})
        return data


class ChangeOldPasswordRequestSerializer(serializers.Serializer):
    """
    Serializer for changing user passwords with old password verification.
    """
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Old Password'}
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'New Password'}
    )
    re_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Confirm New Password'}
    )

    def validate(self, data):
        """
        Validate that password and re_password match.
        """
        if data.get('password') != data.get('re_password'):
            raise serializers.ValidationError({"message": "Passwords do not match"})
        return data


class ChangeUserEmailRequestSerializer(serializers.Serializer):
    """
    Serializer for changing user email.
    """
    old_email = serializers.EmailField(
        write_only=True,
        required=False,
        style={'input_type': 'email', 'placeholder': 'Old Email'}
    )
    new_email = serializers.EmailField(
        write_only=True,
        required=True,
        style={'input_type': 'email', 'placeholder': 'New Email'}
    )

    def validate(self, data):
        """
        Validate that the new email is not already in use.
        """
        new_email = data.get("new_email")
        if new_email and User.objects.filter(email__iexact=new_email).exists():
            raise serializers.ValidationError({"message": "Email already exists"})
        return data
