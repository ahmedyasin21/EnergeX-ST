from rest_framework import generics, status
from rest_framework.response import Response
from accounts import serializers
from accounts.models import Otp
from accounts.utils import custom_send_email
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateUserAPIView(generics.CreateAPIView):
    """
    Endpoint for creating a new user.
    If 'otp_required' flag is True, an OTP will be generated and user
    must verify before activation. Otherwise, user is active immediately.
    """
    serializer_class = serializers.CreateAccountsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp_required = request.data.get("otp_required", False)

        try:
            # Create user inactive only if OTP verification is required
            user = User.objects.create_user(
                username=request.data["username"],
                email=request.data["email"],
                password=request.data["password"]
            )
            user.is_active = True
            user.save()
            if otp_required:
                user.is_active = False
                user.save()

                otp_instance = Otp.objects.create(email=user.email, purpose="sign_up")

                custom_send_email(
                    subject="Sign Up Verification OTP Code - PlayApp Economy",
                    to_email=user.email,
                    template_name="otpVerification.html",
                    context={
                        'user_name': user.username,
                        'otp': otp_instance.otp,
                    }
                )

                return Response(
                    {"message": "User registered successfully. Please verify OTP sent to your email."},
                    status=status.HTTP_201_CREATED
                )

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "User registered successfully."},
            status=status.HTTP_201_CREATED
        )


