from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Cafe
from .serializers import CafeSerializer
from firebase_admin import firestore

class CafeListAPIView(APIView):
    # add permission to check if user is authenticated
    permission_classes = []

    def get(self, request, cafe_id=None):
        if cafe_id is None:
            db = firestore.client()
            cafes_ref = db.collection('cafes')
            cafes = cafes_ref.get()
            cafes_data = {}
            cafe_id = 1
            for cafe in cafes:
                cafe_data = cafe.to_dict()
                cafes_data[cafe_id] = cafe_data
                cafe_id += 1
        
            response_data = {
                "status": 200,
                "data": cafes_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            db = firestore.client()
            cafe_ref = db.collection('cafes').document(cafe_id)
            cafe = cafe_ref.get()
        
            if cafe.exists:
                cafe_data = cafe.to_dict()
                response_data = {
                    "status": 200,
                    "data": cafe_data
                }
            else:
                response_data = {
                    "status": 404,
                    "message": "Cafe not found"
                }
            return Response(response_data, status=status.HTTP_200_OK)
        