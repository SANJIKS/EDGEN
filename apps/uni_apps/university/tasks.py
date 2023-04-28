from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_registration_request(recipient_list, approved):
    if approved:
        subject = 'Ваша заявка одобрена'
        message = """
        Здравствуйте, ваша заявка на становление владельцем одобрена. Спасибо, что выбрали наш сервис!
        """
    else:
        subject = 'Ваша заявка отклонена'
        message = """
        Мы рассмотрели вашу заявку, и вынуждены отказать вам.
        """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False
    )
