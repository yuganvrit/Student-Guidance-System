from rest_framework import serializers
from career.models import CareerPath, Career
from course.models import Course


class CareerPathCreateSerializer(serializers.ModelSerializer):
    career = serializers.PrimaryKeyRelatedField(queryset=Career.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    
    class Meta:
        model = CareerPath
        fields = ['id', 'career', 'course', 'sequence_number']
    
    def validate(self, attrs):
        # Resolve effective values (handle partial updates)
        career = attrs.get('career')
        if career is None and self.instance:
            career = self.instance.career
        
        course = attrs.get('course')
        if course is None and self.instance:
            course = self.instance.course
        
        sequence_number = attrs.get('sequence_number')
        if sequence_number is None and self.instance:
            sequence_number = self.instance.sequence_number
        
        # Check career + course uniqueness
        existing_course = CareerPath.objects.filter(career=career, course=course)
        if self.instance:
            existing_course = existing_course.exclude(pk=self.instance.pk)
        if existing_course.exists():
            raise serializers.ValidationError(
                {"course": "This course is already associated with the selected career."}
            )
        
        # Check career + sequence uniqueness
        existing_seq = CareerPath.objects.filter(career=career, sequence_number=sequence_number)
        if self.instance:
            existing_seq = existing_seq.exclude(pk=self.instance.pk)
        if existing_seq.exists():
            raise serializers.ValidationError(
                {"sequence_number": "This sequence number is already used for the selected career."}
            )
        
        return attrs


class CareerPathReadSerializer(serializers.ModelSerializer):
    career_title = serializers.CharField(source='career.title', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = CareerPath
        fields = ['id', 'career', 'career_title', 'course', 'course_title', 'sequence_number']
