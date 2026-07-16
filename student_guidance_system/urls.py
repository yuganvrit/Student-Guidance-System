"""
URL configuration for student_guidance_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# student_guidance_system/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.views import RegisterView, LoginView, MeView, ProfileView
from course.views import CourseViewSet, CourseBatchViewSet
from appointments.views import AppointmentViewSet
from .views import home     

from assessment.views import QuestionViewSet, AssessmentResultViewSet
from counseling.views import CounselingSessionViewSet
from enrollment.views import EnrollmentViewSet     

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'batches', CourseBatchViewSet, basename='batch')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'assessments', AssessmentResultViewSet, basename='assessment-results')

router.register(r'questions', QuestionViewSet)
router.register(r'assessments', AssessmentResultViewSet)
router.register(r'counseling', CounselingSessionViewSet)
router.register(r'enrollments', EnrollmentViewSet) 

urlpatterns = [
    path('', home, name='home'),                 
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/me/', MeView.as_view(), name='me'),
    path('api/auth/profile/', ProfileView.as_view(), name='profile'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    


   