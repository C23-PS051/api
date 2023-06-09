from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from firebase_admin import firestore

class FavoriteListAPIView(APIView):
    # add permission to check if user is authenticated
    permission_classes = []

    def post(self, request):
        db = firestore.client()
        favorite_ref = db.collection('favorites').document()
        favorite_ref.set(request.data)
        
        response_data = {
            "status": 200,
        }
        return Response(response_data)

