from rest_framework.views import APIView
from authentication.serializers.counselor_register_serializer import CounselorRegisterSerializer
from rest_framework.permissions import IsAdminUser
from utils.response_helpers import error_response, success_response

class CounselorRegisterView(APIView):
    permission_classes=[IsAdminUser]

    def post(self, request):
        serializer = CounselorRegisterSerializer(data = request.data)
        if not serializer.is_valid():
            return error_response(message="Registration failed", errors=serializer.errors, status_code=400)
        serializer.save()
        return success_response(message="User registered successfully" , data=serializer.data, status_code=201)