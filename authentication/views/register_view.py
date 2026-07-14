from rest_framework.views import APIView
from authentication.serializers.register_serializer import RegisterSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)