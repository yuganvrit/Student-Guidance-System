from django.urls import path
from .views import login_view, logout_view, register_view

urlpatterns = [
    path('auth/login',login_view.LoginView.as_view(), name='login' ),
    path('auth/login',register_view.RegisterView.as_view(), name='login' ),
    path('auth/login',logout_view.LogoutView.as_view(), name='login' )
]
