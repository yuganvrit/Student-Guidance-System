from rest_framework.routers import DefaultRouter
from django.urls import path,include
from career.views.career_view import CareerViewSet


router = DefaultRouter()
router.register(r'careers', CareerViewSet, basename='career')

urlpatterns=[
    path('', include(router.urls))
]