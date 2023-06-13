from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from firebase_admin import firestore
from rest_framework.permissions import IsAuthenticated
from auth_api.authentication import FirebaseAuthentication
import json

class FavoriteListAPIView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]

    def get(self, request):
        db = firestore.client()
        favorite_ref = db.collection('favorites')
        cafe_ref = db.collection('cafes')
        favorites = favorite_ref.get()
        user_id = request.user.id
        cafes_result=[]
        
        for favorite in favorites:
            favorite_id = favorite.id
            favorite_data = favorite.to_dict()
            if str(favorite_data['user_id']) == str(user_id):
                cafes_result.append(cafe_ref.document(favorite_data['cafe_id']).get().to_dict())
        response_data = {
            "result": cafes_result,
            "status": 200,
        }
        return Response(response_data)

    def post(self, request):
        db = firestore.client()
        favorite_ref = db.collection('favorites').document()
        favorite_ref.set(request.data)
        
        response_data = {
            "status": 200,
        }
        return Response(response_data)

    def delete(self, request):
        db = firestore.client()
        favorite_ref = db.collection('favorites')
        favorites = favorite_ref.get()
        favorites_data = {}
        body_unicode = request.body.decode('utf-8')
        json_body = json.loads(body_unicode)

        for favorite in favorites:
            favorite_id = favorite.id
            favorite_data = favorite.to_dict()
            favorites_data[favorite_id] = favorite_data
            if favorite_data['cafe_id'] == json_body['cafe_id'] and favorite_data['user_id'] == json_body['user_id']:
                deleted_ref = db.collection('favorites').document(favorite_id)
                response_data = {
                    "status": 200,
                }
                deleted_ref.delete()
                return Response(response_data)

        response_data = {
                    "message": "not found",
                }
        return Response(response_data)
        
        

