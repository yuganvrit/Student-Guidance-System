from django.urls import path

from course.views.course_category_views import (
    CourseCategoryListCreateView,
    CourseCategoryDetailView,
)

urlpatterns = [
    path('categories/', CourseCategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CourseCategoryDetailView.as_view(), name='category-detail'),
]
