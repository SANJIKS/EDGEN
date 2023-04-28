from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_registration_request(recipient_list, approved):
    if approved:
        subject = 'Ваша заявка одобрена'
        message = """
        Здравствуйте, мы зарегистрировали ваш университет в EDGEN, и вы также являетесть владельцема данного университета.
        """
    else:
        subject = 'Ваша заявка отклонена'
        message = """
        Здравствуйте, мы вынуждены отклонить вашу заявку на регистрацию вашего университета в EDGEN, до свидания!.
        """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False
    )


@shared_task
def send_owner_add(user_email, uni_name):
    subject = 'Вы стали совладельцем!'
    message = f"""
    Здраствуйте, вы стали совладельцем универа {uni_name}
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False
    )


@shared_task
def send_owner_delete(user_email, uni_name):
    subject = 'Вы были удалены из совладельцев'
    message = f"""
    Здраствуйте, вы больше не являетесь совладельцем универа {uni_name}
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False
    )


@shared_task
def send_student_inroll(recipient_list, uni_name):
    subject = 'Вы зачислены в универ'
    message = f"""
    Здраствуйте, вы зачислены в универ {uni_name}
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False
    )


@shared_task
def send_student_outroll(recipient_list, uni_name):
    subject = 'Вы удалены из универа'
    message = f"""
    Здраствуйте, вы удалены из универа {uni_name}
    """

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False
    )
