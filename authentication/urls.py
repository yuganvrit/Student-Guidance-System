from django.urls import path
from .views import login_view, logout_view, register_view
from rest_framework_simplejwt.views import  TokenRefreshView

urlpatterns = [
    path('auth/login/',login_view.LoginView.as_view(), name='login' ),
    path('auth/register/',register_view.RegisterView.as_view(), name='register' ),
    path('auth/logout/',logout_view.LogoutView.as_view(), name='logout' ),
    path('auth/refresh/',TokenRefreshView.as_view(), name='token_refresh' )
]
