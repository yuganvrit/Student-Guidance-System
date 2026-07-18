from django.urls import path
from .views import login_view, logout_view, counselor_register_view, mentor_register_view, student_register_view
from rest_framework_simplejwt.views import  TokenRefreshView

urlpatterns = [
    path('auth/login/',login_view.LoginView.as_view(), name='login' ),
    path('auth/counselor/register/',counselor_register_view.CounselorRegisterView.as_view(), name='counselor_register' ),
    path('auth/mentor/register/',mentor_register_view.MentorRegisterView.as_view(), name='mentor_register' ),
    path('auth/student/register/',student_register_view.StudentRegisterView.as_view(), name='student_register' ),
    path('auth/logout/',logout_view.LogoutView.as_view(), name='logout' ),
    path('auth/refresh/',TokenRefreshView.as_view(), name='token_refresh' )
]
