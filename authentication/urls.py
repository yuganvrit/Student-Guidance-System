from django.urls import path, include
from .views import login_view, logout_view, counselor_register_view, mentor_register_view, student_register_view
from rest_framework_simplejwt.views import  TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'auth/students', student_register_view.StudentViewSet, basename='student')
router.register(r'auth/mentors', mentor_register_view.MentorViewSet, basename='mentor')
router.register(r'auth/counselors', counselor_register_view.CounselorViewSet, basename='counselor')

urlpatterns = [
    path('auth/login/',login_view.LoginView.as_view(), name='login' ),
    # path('auth/counselors/register/',counselor_register_view.CounselorRegisterView.as_view(), name='counselor_register' ),
    # path('auth/mentors/register/',mentor_register_view.MentorViewSet.as_view(), name='mentor_register' ),
    path('', include(router.urls)),
    path('auth/logout/',logout_view.LogoutView.as_view(), name='logout' ),
    path('auth/refresh/',TokenRefreshView.as_view(), name='token_refresh' )
]
