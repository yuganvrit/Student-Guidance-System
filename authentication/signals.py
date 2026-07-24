from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StudentProfile
from .tasks import send_welcome_email_task


# @receiver(post_save, sender=User)
# def send_welcome_mail(sender, instance, created, **kwargs):
#     if created:
#         StudentProfile.objects.create(student=instance)
#         send_welcome_email_task.delay(instance.email, instance.first_name)
