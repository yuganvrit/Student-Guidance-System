# authentication/views/mentor_view.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from authentication.models import User
from authentication.serializers.mentor_register_serializer import (
    MentorRegisterSerializer,
    MentorUpdateSerializer,
    MentorUserMiniSerializer
)
from utils.response_helpers import error_response, success_response
from authentication.tasks import send_welcome_email


class MentorViewSet(viewsets.ModelViewSet):
    """
    Handles mentor CRUD operations:
    - list, retrieve, update, partial_update, destroy
    - custom register action for public mentor registration
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            role='mentor',
            is_deleted=False
        ).select_related('mentor_profile').prefetch_related('mentor_profile__skills')

    def get_serializer_class(self):
        if self.action == 'register':
            return MentorRegisterSerializer
        if self.action == 'list':
            return MentorUserMiniSerializer
        return MentorUpdateSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Public registration endpoint for new mentors"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_welcome_email.delay(user.email, user.first_name)
        return success_response(
            message="Mentor registered successfully",
            data=MentorUpdateSerializer(user).data,
            status_code=status.HTTP_201_CREATED
        )
        
    def create(self, request, *args, **kwargs):
        """Block the default create action."""
        return error_response(
            message="Use /register/ endpoint instead.",
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED
        )