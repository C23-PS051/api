from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
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
        user = db.collection('users').document(current_username).get().to_dict()
        
        ML_API_URL = os.getenv("ML_API_URL")
        
        payload = {
            "new_user_id": current_username, 
            "new_is_male": 1, # placeholder
            "new_age_group": 1, # placeholder
            "new_price_category": 1 if user["cafe_price_category"]=="$" else (2 if user["cafe_price_category"]=="$$" else 3),
            "new_24hrs": 1, # placeholder
            "new_outdoor": 1 if user["cafe_outdoor"] else 0,
            "new_smoking_area": 1 if user["cafe_smoking_area"] else 0,
            "new_parking_area": 1 if user["cafe_parking_area"] else 0,
            "new_pet_friendly": 1 if user["cafe_pet_friendly"] else 0,
            "new_wifi": 1 if user["cafe_wifi"] else 0,
            "new_indoor": 1 if user["cafe_indoor"] else 0,
            "new_live_music": 1 if user["cafe_live_music"] else 0,
            "new_takeaway": 1 if user["cafe_takeaway"] else 0,
            "new_kid_friendly": 1 if user["cafe_kid_friendly"] else 0,
            "new_alcohol": 1 if user["cafe_alcohol"] else 0,
            "new_in_mall": 1 if user["cafe_in_mall"] else 0,
            "new_toilets": 1 if user["cafe_toilets"] else 0,
            "new_reservation": 1 if user["cafe_reservation"] else 0,
            "new_vip_room": 1 if user["cafe_vip_room"] else 0
        }

        res = requests.post(ML_API_URL, json=payload)

        print(res.text)
        response_data = {
            "status": 200,
            "data": res.json()
        }

        return Response(response_data, status=status.HTTP_200_OK)
        