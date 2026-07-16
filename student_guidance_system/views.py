# student_guidance_system/views.py
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Welcome to the Student Guidance System API",
        "endpoints": {
            "auth": "/api/auth/",
            "courses": "/api/courses/",
            "batches": "/api/batches/",
            "appointments": "/api/appointments/",
            "admin": "/admin/"
        }
    })