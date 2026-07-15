from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from authentication.utils.response_helpers import error_response, success_response

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh = request.data.get('refresh')
            if refresh:
                token = RefreshToken(refresh)
                token.blacklist()
                return success_response(message='successfully logged out', status_code=204)
            return error_response(message='token required', status_code=400)
        except Exception as e:
            return error_response(errors=str(e), status_code=403)