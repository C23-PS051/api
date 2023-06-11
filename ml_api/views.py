from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Cafe
from .serializers import CafeSerializer
from firebase_admin import firestore
from rest_framework.permissions import IsAuthenticated
from auth_api.authentication import FirebaseAuthentication
import requests
import os

class RecommendationAPIView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]

    def get(self, request):
        current_username = request.user.username
        db = firestore.client()
        user = db.collection('users').document(current_username)
        
        ML_API_URL = os.getenv("ML_API_URL")
        
        payload = {
            "new_user_id": current_username, 
            "new_is_male": True, # placeholder
            "new_age_group": 1, # placeholder
            "new_price_category": user.cafe_price_category,
            "new_24hrs": True,
            "new_outdoor": user.cafe_outdoor,
            "new_smoking_area": user.cafe_smoking_area,
            "new_parking_area": user.cafe_parking_area,
            "new_pet_friendly": user.cafe_pet_friendly,
            "new_wifi": user.cafe_wifi,
            "new_indoor": user.cafe_indoor,
            "new_live_music": user.cafe_live_music,
            "new_takeaway": user.cafe_takeaway,
            "new_kid_friendly": user.cafe_kid_friendly,
            "new_alcohol": user.cafe_alcohol,
            "new_in_mall": user.cafe_in_mall,
            "new_toilets": user.cafe_toilets,
            "new_reservation": user.cafe_reservations,
            "new_vip_room": user.cafe_vip_room
        }

        res = requests.post(ML_API_URL, json=payload)

        response_data = {
            "status": 200,
            "data": res.json
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        