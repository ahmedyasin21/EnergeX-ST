from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from .managers import UserManager,OtpManager
from django.utils import timezone

class CustomUser(AbstractBaseUser):
    
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=100,
        db_column="user_name",
        unique=True,
        help_text=_('Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    phone_no =  models.CharField(_('Phone number'),max_length=100, unique=True,null=True,blank=True,
        error_messages={
            'unique': _("A user with that phone number already exists."),
        },

    )

    is_active =  models.BooleanField(_("is active"),default=False)
    staff = models.BooleanField(_("is Staff"),db_column="is_staff", default=False)
    admin = models.BooleanField(_("admin bool flag"), db_column="is_admin", default=False)

    referrer_user = models.CharField(_("referrer_user"), max_length=50,null=True,blank=True)

    is_remove = models.BooleanField(_("Remove"), default=False)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    create_time = models.DateTimeField(_("Created Time"), default = timezone.now)
    update_time = models.DateTimeField(_("Updated Time"), default = timezone.now)
    
    

    class Meta:
        db_table = "platform_user"
        verbose_name = _("User")
        verbose_name_plural = ("Users")
        

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"] # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


class Otp(models.Model):

    class Purposes(models.TextChoices):
        SIGN_UP = 'sign_up', _('Sign_up')
        FORGOT_PASSWORD = 'forget_password', _('Forget_password')
        RESET_PASSWORD = 'reset_password', _('Reset_password')
        CHANGE_EMAIL = 'change_email', _('Change_email')
        VERIFY_ACCOUNT = 'verify_account', _('Verify_account')
        RESEND_OTP = 'resend_otp', _('Resend_otp')





    email = models.EmailField(_("Email"), max_length=254)
    expire = models.BooleanField(_("expire"),default=False)
    otp = models.IntegerField(_("otp"),null=True,blank=True)
    purpose = models.CharField(_("Purposes"), choices=Purposes.choices ,max_length=50, null=True, blank=True)
    ttl = models.DateTimeField(_("time to live"), null=True,blank=True)
    is_remove = models.BooleanField(_("removed"),default=False)
    update = models.DateTimeField(_("update time"), null=True,blank=True)

    create_time = models.DateTimeField(_("create time"), default=timezone.now)

    objects = OtpManager()


    class Meta:
        db_table = "otp"
        verbose_name = _("otp")

    def __str__(self):
        return self.email





