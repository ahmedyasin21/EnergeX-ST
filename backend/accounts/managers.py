from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.apps import apps
from accounts.querysets import UserQuerySet, OtpQuerySet
import random
from accounts.utils import check_email, is_valid_phone_number
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    """Custom manager for User model."""

    def get_queryset(self):
        return UserQuerySet(self.model, using="default")

    def create_user(self, username, email, phone_no=None, password=None, referrer_user=None, **extra_fields):
        """
        Creates and saves a User with the given username, email, and password.
        """
        if not username or " " in username:
            raise ValidationError('Username is required.' if not username else 'Username should not contain spaces.')

        username = username.lower()
        if self.get_queryset().filter(username=username).exists():
            raise ValidationError('A user with that username already exists.')

        if not email:
            raise ValidationError('Email address is required.')

        email = email.lower()
        if self.get_queryset().filter(email=email).exists():
            raise ValidationError('A user with that email already exists.')

        if not check_email(email):
            raise ValidationError('Invalid email address.')

        if phone_no:
            phone_no = f"+{phone_no.lstrip('+')}"  # Ensure phone_no starts with "+"
            if not is_valid_phone_number(phone_no):
                raise ValidationError('Invalid phone number.')
            # Uncomment below if phone number uniqueness is required
            # if self.get_queryset().filter(phone_no=phone_no).exists():
            #     raise ValidationError('A user with that phone number already exists.')

        if password:
            if " " in password:
                raise ValidationError('Password should not contain spaces.')
            try:
                validate_password(password, self.model(**extra_fields))
            except ValidationError as e:
                raise ValidationError(" ".join(e.messages[:3]))

        # Normalize username and create the user
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone_no=phone_no,
            referrer_user=referrer_user,
        )
        user.set_password(password)
        user.is_active = True
        user.save(using="default")
        
        return user

    def create_staffuser(self, username, email, password=None, **extra_fields):
        """Creates and saves a staff user."""
        user = self.create_user(username=username, email=email, password=password, **extra_fields)
        user.is_active = True
        user.staff = True
        user.save(using="default")
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Creates and saves a superuser."""
        user = self.create_user(username=username, email=email, password=password, **extra_fields)
        user.is_active = True
        user.staff = True
        user.admin = True
        user.save(using="default")
        return user

    def custom_save(self, obj):
        """Save using the default database."""
        obj.save(using="default")
        return obj

    # Utility functions
    def get_user_by_id(self,id):
        return self.get_queryset().get_user_by_id(id)

    def get_user_by_username(self,username):
        return self.get_queryset().get_user_by_username(username)

    def just_get_user_by_username(self,username):
        return self.get_queryset().just_get_user_by_username(username)

    def get_user_by_email(self,email):
        return self.get_queryset().get_user_by_email(email)
    
    def get_user_by_phone_no(self,phone_no):
        return self.get_queryset().get_user_by_phone_no(phone_no)
    
    def get_all_users_by_referrer_user(self,referrer_user):
        return self.get_queryset().get_all_users_by_referrer_user(referrer_user)


class OtpManager(models.Manager):
    """Manager for handling OTP creation and validation."""

    def get_queryset(self):
        return OtpQuerySet(self.model, using="default")

    def create(self, email, purpose, ttl=None, otp=None):
        """
        Creates a new OTP entry.
        """
        if not email:
            raise ValidationError('Email is required.')

        if not check_email(email):
            raise ValidationError('Invalid email address.')

        # Expire previous OTPs for the given email
        self.get_queryset().filter(email=email).update(expire=True)

        otp = otp or self.generate_otp()
        ttl = ttl or timezone.localtime(timezone.now()) + timedelta(seconds=120)

        otp_instance = self.model(
            email=email,
            otp=otp,
            purpose=purpose,
            ttl=ttl,
        )
        otp_instance.save(using="default")
        return otp_instance

    def generate_otp(self, length=6):
        """Generate a unique OTP of the given length."""
        while True:
            generated_otp = random.randint(10**(length-1), 10**length - 1)
            if not self.if_exists_by_otp(generated_otp):
                return generated_otp

    def if_exists(self,id):
        return self.get_queryset().if_exists(id)

    def if_exists_by_email(self,email):
        return self.get_queryset().if_exists_by_email(email)

    def if_exists_by_otp(self,otp):
        return self.get_queryset().if_exists_by_otp(otp)
    
    def if_expired(self,otp):
        return self.get_queryset().if_expired(otp)

    def opt_expire_list(self):
        return self.get_queryset().opt_expire_list()


    def opt_to_be_removed_list(self):
        return self.get_queryset().opt_to_be_removed_list()

    def get_all_with_email(self,email):
        return self.get_queryset().get_all_with_email(email)
    
    
    def custom_save(self, obj):
        """Save using the default database."""
        obj.save(using="default")
        return obj
