from rest_framework.routers import DefaultRouter
from counselling.views.counsellingSession import CounselingSessionViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'counselling-sessions', CounselingSessionViewSet, basename='counselling-session')

urlpatterns = [
    path('', include(router.urls))
]