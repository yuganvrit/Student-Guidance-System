from rest_framework import serializers
from course.models import Course, CourseCategory
from .course_category_serializer import GetMiniCourseCategorySerializer

class CourseSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CourseCategory.objects.all()
    )
    class Meta:
        model=Course
        fields = "__all__"



    def validate(self,attrs):
        categories = attrs.get('categories')
        if not categories:
            raise serializers.ValidationError('Categories cannot be empty')
        return attrs

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        course = Course.objects.create(**validated_data)
        course.categories.set(categories)
        return course

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categories is not None:
            instance.categories.set(categories)
        return instance


class GetCourseSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = "__all__"

    def get_categories(self,obj):
        return GetMiniCourseCategorySerializer(obj.categories.all(),many=True).data
    

class GetMiniCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','title']
