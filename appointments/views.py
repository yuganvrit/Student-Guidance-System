# appointments/views.py
from rest_framework import viewsets, permissions, filters
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentDetailSerializer

class IsStudentOrAdvisor(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow students, advisors, and super_admin
        return request.user.role in ['student', 'advisor', 'super_admin']

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.filter(is_deleted=False)
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudentOrAdvisor]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['status', 'notes']
    ordering_fields = ['scheduled_time', 'created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AppointmentDetailSerializer
        return AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # Role-based filtering
        if user.role == 'student':
            queryset = queryset.filter(student=user)
        elif user.role == 'advisor':
            queryset = queryset.filter(advisor=user)
        # super_admin gets all

        # Extra query parameters
        student_id = self.request.query_params.get('student_id')
        advisor_id = self.request.query_params.get('advisor_id')
        status_filter = self.request.query_params.get('status')
        
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if advisor_id:
            queryset = queryset.filter(advisor_id=advisor_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset

    def perform_create(self, serializer):
        # If logged-in user is a student, force the appointment to be for them
        if self.request.user.role == 'student':
            serializer.save(student=self.request.user)
        else:
            serializer.save()