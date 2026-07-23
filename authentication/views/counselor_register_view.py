# authentication/views/counselor_view.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from authentication.models import User
from authentication.serializers.counselor_register_serializer import (
    CounselorRegisterSerializer,
    CounselorUpdateSerializer,
    CounselorUserMiniSerializer
)
from utils.response_helpers import error_response, success_response
from authentication.tasks import send_welcome_email


class CounselorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            role='counselor',
            is_deleted=False
        ).select_related('counselor_profile')

    def get_serializer_class(self):
        if self.action == 'register':
            return CounselorRegisterSerializer
        if self.action == 'list':
            return CounselorUserMiniSerializer
        return CounselorUpdateSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_welcome_email.delay(user.email, user.first_name)
        return success_response(
            message="Counselor registered successfully",
            data=CounselorUpdateSerializer(user).data,
            status_code=status.HTTP_201_CREATED
        )
        
    def create(self, request, *args, **kwargs):
        return error_response(
            message="Use /register/ endpoint instead.",
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED
        )