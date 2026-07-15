from django.urls import path

from course.views import course_category_views, course_batch_views, course_views



urlpatterns = [
    path('course/', course_views.CourseListCreateView.as_view(), name='course-list-create'),
    path('course/<int:pk>/', course_views.CourseDetailView.as_view(), name='course-detail'),
    path('course/categories/', course_category_views.CourseCategoryListCreateView.as_view(), name='category-list-create'),
    path('course/categories/<int:pk>/', course_category_views.CourseCategoryDetailView.as_view(), name='category-detail'),
    path('course/batches/', course_batch_views.CourseBatchListCreateView.as_view(), name='course-batch'),
    path('course/batches/<int:pk>/', course_batch_views.CourseBatchDetailView.as_view(), name='course-batch-detail'),
]