from rest_framework.routers import DefaultRouter
from django.urls import path,include
from career.views import career_view, career_path_view


router = DefaultRouter()
router.register(r'careers', career_view.CareerViewSet, basename='career')
router.register(r'career-paths', career_path_view.CareerPathViewSet, basename='career-path')

urlpatterns=[
    path('', include(router.urls))
]