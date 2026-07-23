# student_guidance_system/celery.py
import os
from celery import Celery

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_guidance_system.settings')

# Create Celery app
app = Celery('student_guidance_system')

# Load config from Django settings (CELERY_* variables)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()