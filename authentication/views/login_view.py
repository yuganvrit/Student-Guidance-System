# from rest_framework_simplejwt.views import TokenObtainPairView
# from authentication.serializers.login_serializer import LoginSerializer

# class LoginView(TokenObtainPairView):

#     serializer_class = LoginSerializer



#using apiview
from rest_framework.views import APIView
from authentication.serializers.login_serializer import LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        data={
            'user':{
                'user_id':user.id,
                'username':user.username,
                'email':user.email
            },
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
        
        return Response(data, status=status.HTTP_200_OK)