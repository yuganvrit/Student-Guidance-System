from rest_framework.routers import DefaultRouter
from django.urls import path, include
from skill.views.skill_view import SkillViewSet

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')

urlpatterns = [
    path('', include(router.urls))
]