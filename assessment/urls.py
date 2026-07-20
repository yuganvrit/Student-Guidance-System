from django.urls import path, include
from rest_framework.routers import DefaultRouter
from assessment.views import assessment_view, assessment_skill_view, student_assessment_view

router = DefaultRouter()
router.register(r'assessments', assessment_view.AssessmentViewSet, basename='assessment')
router.register(r'assessment-skills', assessment_skill_view.AssessmentSkillViewSet, basename='assessment-skill')
router.register(r'student-assessments', student_assessment_view.StudentAssessmentViewSet, basename='student-assessment')

urlpatterns=[
    path('', include(router.urls))
]