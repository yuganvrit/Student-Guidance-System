from rest_framework.routers import DefaultRouter
from counselling.views import counsellingSession, student_counselor_view
from django.urls import path, include

router = DefaultRouter()
router.register(r'counselling-sessions', counsellingSession.CounselingSessionViewSet, basename='counselling-session')
router.register(r'student-counselors', student_counselor_view.StudentCounselorViewSet, basename='student-counselor')

urlpatterns = [
    path('', include(router.urls))
]