from rest_framework import viewsets
from counselling.models import StudentCounselor
from counselling.serializers.student_counselor_serializer import StudentCounselorReadSerializer, StudentCounselorWriteSerializer


class StudentCounselorViewSet(viewsets.ModelViewSet):
    queryset = StudentCounselor.objects.all()
    permission_classes = []

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return StudentCounselorReadSerializer
        return StudentCounselorWriteSerializer