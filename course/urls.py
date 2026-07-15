from django.urls import path,include 
from rest_framework.routers import DefaultRouter
from course.views import course_category_views, course_batch_views, course_views


router = DefaultRouter()
router.register(r'categories',course_category_views.CourseCategoryViewset)
urlpatterns = [
    path('course/', course_views.CourseListCreateView.as_view(), name='course-list-create'),
    path('course/<int:pk>/', course_views.CourseDetailView.as_view(), name='course-detail'),
    path('course/batches/', course_batch_views.CourseBatchListCreateView.as_view(), name='course-batch'),
    path('course/batches/<int:pk>/', course_batch_views.CourseBatchDetailView.as_view(), name='course-batch-detail'),
    path('course/', include(router.urls))
]