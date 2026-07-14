# from rest_framework_simplejwt.views import TokenObtainPairView
# from authentication.serializers.login_serializer import LoginSerializer

# class LoginView(TokenObtainPairView):

#     serializer_class = LoginSerializer



#using apiview
from rest_framework.views import APIView
from authentication.serializers.login_serializer import LoginSerializer
from rest_framework.response import Response
from rest_framework import status

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)