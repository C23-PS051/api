from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from auth_api.authentication import FirebaseAuthentication


# Create your views here.
class TestAuthenticatedAPIView(APIView):
    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]

    def get(self, request):
        return Response({"status": 200})