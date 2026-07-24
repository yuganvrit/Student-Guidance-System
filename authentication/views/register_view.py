from rest_framework.views import APIView
from authentication.serializers.register_serializer import RegisterSerializer
from rest_framework.permissions import AllowAny
from authentication.utils.response_helpers import error_response, success_response
from ..tasks import send_welcome_email_task


class RegisterView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data = request.data)
        if not serializer.is_valid():
            return error_response(message="Registration failed", errors=serializer.errors, status_code=400)
        user = serializer.save()
        send_welcome_email_task.delay(user.email,user.first_name)
        return success_response(message="User registered successfully" , data=serializer.data, status_code=201)