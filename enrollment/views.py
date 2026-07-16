from rest_framework import viewsets, permissions
from .models import Enrollment
from .serializers import EnrollmentSerializer, EnrollmentDetailSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.filter(is_deleted=False)
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EnrollmentDetailSerializer
        return EnrollmentSerializer

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == 'student':
            qs = qs.filter(student=user)
        return qs

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)