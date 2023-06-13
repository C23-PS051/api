from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Cafe
from .serializers import CafeSerializer
from firebase_admin import firestore
from rest_framework.permissions import IsAuthenticated
from auth_api.authentication import FirebaseAuthentication

class CafeListAPIView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]

    def get(self, request, cafe_id=None):
        if cafe_id is None:
            db = firestore.client()
            cafes_ref = db.collection('cafes')

            # Search
            search_query = request.GET.get('search', '')
            if search_query:
                search_query = search_query.lower()
                cafes = cafes_ref.get()
                cafes_data = []
        
                for cafe in cafes:
                    cafe_data = cafe.to_dict()
                    if cafe_data['name'].lower().find(search_query) > -1 :
                        cafes_data.append(cafe_data)
                response_data = {
                    "status": 200,
                    "data": cafes_data
                }
                return Response(response_data, status=status.HTTP_200_OK)
    
            # Filtering
            filter_params = request.GET.getlist('filter')
            for param in filter_params:
                cafes_ref = cafes_ref.where(param, '==', True)
            min_rating = request.GET.get('min_rating', '')
            if min_rating:
                min_rating = float(min_rating)
                cafes_ref = cafes_ref.where('rating', '>=', min_rating)
                
            # Ordering
            order_query = request.GET.get('order', '')
            reverse_order = request.GET.get('reverse', '') == 'true'
            if order_query:
                cafes_ref = cafes_ref.order_by(order_query, direction=firestore.Query.DESCENDING if reverse_order else firestore.Query.ASCENDING)

            cafes = cafes_ref.get()
            cafes_data = []
            for cafe in cafes:
                cafe_data = cafe.to_dict()
                cafe_data["cafe_id"] = cafe.id
                cafes_data.append(cafe_data)
        
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
                cafe_data["cafe_id"] = cafe.id
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
        