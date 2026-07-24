# authentication/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task()
def send_welcome_email( user_email, user_first_name):

    send_mail(
            subject='Welcome to Student Guidance System!',
            message=f'Hi {user_first_name},\n\nYour account has been created successfully.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
    return f"Welcome email sent to {user_email}"
    
