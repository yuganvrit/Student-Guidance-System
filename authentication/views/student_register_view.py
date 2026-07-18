from rest_framework.views import APIView
from authentication.serializers.student_register_serializer import StudentRegisterSerializer
from rest_framework.permissions import AllowAny
from utils.response_helpers import error_response, success_response

class StudentRegisterView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        serializer = StudentRegisterSerializer(data = request.data)
        if not serializer.is_valid():
            return error_response(message="Registration failed", errors=serializer.errors, status_code=400)
        serializer.save()
        return success_response(message="User registered successfully" , data=serializer.data, status_code=201)