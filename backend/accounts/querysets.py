from django.db import models
from datetime import timedelta
from django.utils import timezone

class UserQuerySet(models.QuerySet):
    def get_all(self):
        return self.all().order_by("-create_time")

    def get_user_by_id(self, id):
        try:
            return self.filter(id=id, is_remove=False)[0]
        except IndexError:
            return None

    def get_user_by_username(self, username):
        try:
            return self.filter(username=username, is_remove=False)[0]
        except IndexError:
            return None

    def just_get_user_by_username(self, username):
        try:
            return self.filter(username=username)[0]
        except IndexError:
            return None

    def get_user_by_email(self, email):
        try:
            return self.filter(email=email)[0]
        except IndexError:
            return None

    def get_user_by_phone_no(self, phone_no):
        try:
            return self.filter(phone_no=phone_no, is_active=True, is_remove=False)[0]
        except IndexError:
            return None

    def get_all_users_by_referrer_user(self, referrer_user):
        return self.filter(referrer_user=referrer_user, is_active=True, is_remove=False)

class OtpQuerySet(models.QuerySet):
    def get_all(self):
        return self.all().order_by("-create_time")

    def if_exists(self, id):
        try:
            return self.get(id=id, expire=False, is_remove=False)
        except self.model.DoesNotExist:
            return None

    def if_exists_by_email(self, email):
        try:
            return self.get(email=email, expire=False, is_remove=False)
        except self.model.DoesNotExist:
            return None

    def if_exists_by_otp(self, otp):
        try:
            return self.get(otp=otp, is_remove=False)
        except self.model.DoesNotExist:
            return None

    def if_expired(self, otp):
        try:
            return self.get(otp=otp, ttl__lte=timezone.now(), expire=False, is_remove=False)
        except self.model.DoesNotExist:
            return None

    def get_all_with_email(self, email):
        return self.filter(email=email, expire=False, is_remove=False)

    def opt_expire_list(self):
        return self.filter(
            create_time__range=(timezone.now() - timedelta(days=3550), timezone.now() - timedelta(seconds=120)),
            expire=False,
            is_remove=False
        )

    def opt_to_be_removed_list(self):
        return self.filter(
            create_time__range=(timezone.now() - timedelta(days=3550), timezone.now() - timedelta(seconds=1800)),
            expire=False,
            is_remove=False
        )
