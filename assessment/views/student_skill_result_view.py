# assessment/views/student_skill_result_view.py
from rest_framework import generics, mixins, permissions
from assessment.models import StudentSkillResult
from assessment.serializers.student_skill_result_serializer import StudentSkillResultSerializer


class StudentSkillResultListView(mixins.ListModelMixin, generics.GenericAPIView):
    """
    GET /api/skill-results/
    
    Returns skill results. Students see their own. 
    Counselors see assigned students. Admins see all.
    """
    serializer_class = StudentSkillResultSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    queryset=StudentSkillResult.objects.filter(
                student_assessment__status='completed'
            ).select_related('skill', 'student_assessment__assessment')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)