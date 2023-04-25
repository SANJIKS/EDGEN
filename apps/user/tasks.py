from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from djoser.conf import settings as djoser_settings

User = get_user_model()


@shared_task
def send_registration(user_id, context):
    user = User.objects.get(pk=user_id)
    domain = context['domain']
    activation_link = domain + djoser_settings.ACTIVATION_URL.format(**context)

    subject = 'Activate Your Account'
    message = f"""
    Hello {user.username},
    please click the following link to activate your account:
    {activation_link}
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )


@shared_task
def send_reset_password(user_id, context):
    user = User.objects.get(pk=user_id)
    domain = context['domain']
    activation_link = domain + djoser_settings.PASSWORD_RESET_CONFIRM_URL.format(**context)

    subject = 'Reset password'
    message = f"""
    Hello {user.username},
    there was a request to reset your password, proceed this link to reset your password:
    {activation_link}

    IF YOU DIDN'T REQUESTED TO RESET YOUR PASSWORD, PLEASE IGNORE THIS MESSAGE.
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )


@shared_task
def send_reset_username(user_id, context):
    user = User.objects.get(pk=user_id)
    domain = context['domain']
    activation_link = domain + djoser_settings.USERNAME_RESET_CONFIRM_URL.format(**context)

    subject = 'Reset username'
    message = f"""
    Hello {user.username},
    there was a request to reset your username, proceed this link to reset your username:
    {activation_link}

    IF YOU DIDN'T REQUESTED TO RESET YOUR USERNAME, PLEASE IGNORE THIS MESSAGE.
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )
