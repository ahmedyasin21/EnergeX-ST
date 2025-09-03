import re
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from disposable_email_checker.validators import validate_disposable_email
import accounts
import secrets

def custom_send_email(subject, to_email, template_name, context=None, file=None):
    """
    Sends an email using the specified template and context.
    
    :param subject: Subject of the email.
    :param to_email: Recipient email address.
    :param template_name: Name of the email template.
    :param context: Dictionary containing dynamic values for the template.
    :param file: File to attach (if any).
    :return: True if the email was sent successfully, otherwise False.
    """
    if not template_name:
        return None
    
    context = context or {}
    try:
        template = get_template(template_name)
        html_content = template.render(context)
        
        msg = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email]
        )
        msg.content_subtype = 'html'
        
        if file:
            msg.attach(file.name, file.read(), file.content_type)
        
        msg.send()
        print("Email sent successfully")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        raise ValueError(f"Unable to Sending Email: {e}")
# Regular expression pattern for validating email addresses
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def check_email(email):
    """
    Validates an email address format and checks if it is disposable.
    
    :param email: Email address to validate.
    :return: True if the email is valid and not disposable, otherwise False.
    """
    if re.match(EMAIL_REGEX, email):
        try:
            validate_disposable_email(email)
            return True
        except Exception:
            return False
    print("Invalid Email")
    return False

def resend_otp_func(subject, email, purpose):
    """
    Resends an OTP email for verification purposes.
    
    :param subject: Email subject.
    :param email: Recipient email address.
    :param purpose: Purpose of the OTP.
    """
    try:
        otp_instance = accounts.models.Otp.objects.create(email=email, purpose=purpose)
        if not otp_instance:
            raise ValueError("Request could not be processed. Please try again.")
        
        context = {
            'user_name': email,
            'otp': otp_instance.otp,
        }
        
        custom_send_email(subject=subject, to_email=email, template_name="resendVerification.html", context=context)
    except Exception as e:
        print(f"Error resending OTP: {e}")
        raise e

def is_valid_phone_number(phone_number):
    """
    Validates a Pakistani phone number format (+92XXXXXXXXXX).
    
    :param phone_number: Phone number string.
    :return: True if the phone number is valid, otherwise False.
    """
    return bool(re.match(r'^\+92\d{10}$', phone_number))



def generate_unique_referral_code(username):
    """
    Generates a unique referral code for a new user.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    while True:
        generated_code = f"{username}{secrets.token_hex(3)}"
        if not User.objects.get_user_by_username(generated_code):
            return generated_code