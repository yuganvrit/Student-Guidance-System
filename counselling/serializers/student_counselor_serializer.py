from counselling.models import StudentCounselor
from rest_framework import serializers
from authentication.models import User

class StudentCounselorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCounselor
        fields = '__all__'
        
class StudentCounselorWriteSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='student'))
    counselor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='counselor'))
    class Meta:
        model = StudentCounselor
        fields = '__all__'
        
    def validate(self, attrs):
        student = attrs.get('student')
        is_active= attrs.get('is_active', True)
        if is_active :
            existing = StudentCounselor.objects.filter(student=student, is_active=True)
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise serializers.ValidationError("This student already has an active counselor.")
        return attrs