from django.urls import path, include
from rest_framework.routers import DefaultRouter
from enrollment.views.enrollment_view import EnrollmentView 

router = DefaultRouter()
router.register(r'enrollments', EnrollmentView, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
]