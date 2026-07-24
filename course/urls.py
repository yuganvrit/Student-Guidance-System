from django.urls import path, include

from course.views import course_category_views, course_batch_views, course_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', course_views.CourseView, basename='course')
router.register(r'batches', course_batch_views.CourseBatchView, basename='batch')
router.register(r'categories', course_category_views.CourseCategoryView, basename='category')

urlpatterns = [
    path('', include(router.urls))
]