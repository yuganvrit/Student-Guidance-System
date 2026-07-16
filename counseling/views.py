from rest_framework import viewsets, permissions, filters
from .models import CounselingSession
from .serializers import CounselingSessionSerializer, CounselingSessionDetailSerializer

class CounselingSessionViewSet(viewsets.ModelViewSet):
    queryset = CounselingSession.objects.filter(is_deleted=False)
    serializer_class = CounselingSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['status', 'notes']
    ordering_fields = ['scheduled_time']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CounselingSessionDetailSerializer
        return CounselingSessionSerializer

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == 'student':
            qs = qs.filter(student=user)
        elif user.role == 'advisor':
            qs = qs.filter(counselor=user)
        return qs

    def perform_create(self, serializer):
        if self.request.user.role == 'student':
            serializer.save(student=self.request.user)
        else:
            serializer.save()