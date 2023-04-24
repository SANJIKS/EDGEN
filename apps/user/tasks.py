from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


@shared_task
def send_activation_email(user_id, context):
    user = User.objects.get(pk=user_id)
    activation_link = f"{settings.HOST}/{settings.DJOSER['ACTIVATION_URL'].format(**context)}"
    subject = 'Activate Your Account'
    message = f"""
    Hello {user.username},
    please click the following link to activate your account:
    {activation_link}"""
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )
