from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from ..university.models import University


@shared_task
def send_news(recipient_list, university_id, news_id):
    university = University.objects.get(id=university_id)
    news_link = f'http://{settings.BASE_URL}/news/{news_id}/'
    subject = 'News from your university'
    message = f"""
    Hello dear student!,
    your university {university.name} has new news!
    {news_link}
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False
    )
