from django.urls import path, include
from rest_framework.routers import DefaultRouter
from assessment.views.assessment_view import AssessmentViewSet

router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet, basename='assessment')

urlpatterns=[
    path('', include(router.urls))
]