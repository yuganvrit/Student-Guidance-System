from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_welcome_email_task(email, first_name):
    send_mail(
        subject='Welcome to Student Guidance System',
        message=f'Hi {first_name or email},\n\nYour account has been created successfully.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )
