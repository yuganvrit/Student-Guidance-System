from rest_framework import serializers 
from counselling.models import CounselingSession, StudentCounselor


class CounselingSessionReadSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source='student_counselor.student.username', read_only=True)
    counselor = serializers.CharField(source='student_counselor.counselor.username', read_only=True)
    class Meta:
        model = CounselingSession
        fields = ('id', 'student', 'counselor', 'scheduled_at', 'status', 'notes')
        
class CounselingSessionWriteSerializer(serializers.ModelSerializer):
    student_counselor = serializers.PrimaryKeyRelatedField(queryset=StudentCounselor.objects.filter(is_active=True))
    class Meta:
        model = CounselingSession
        fields = ('student_counselor', 'scheduled_at', 'status', 'notes')
