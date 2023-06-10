from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from firebase_admin import firestore
from rest_framework.permissions import IsAuthenticated
from auth_api.authentication import FirebaseAuthentication

class UserListAPIView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [ IsAuthenticated ]
    authentication_classes = [ FirebaseAuthentication ]

    def get(self, request, user_id):
        db = firestore.client()
        user_ref = db.collection('users').document(user_id)
        user = user_ref.get()
        
        if user.exists:
            user_data = user.to_dict()
            response_data = {
                "status": 200,
                "data": user_data
            }
        else:
            response_data = {
                "status": 404,
                "message": "user not found"
            }
        
        return Response(response_data)

    def put(self, request, user_id):
        db = firestore.client()
        db.collection('users').document(user_id).update(request.data)
        user_ref = db.collection('users').document(user_id)
        user = user_ref.get()
        
        if user.exists:
            user_data = user.to_dict()
            response_data = {
                "status": 200,
                "data": user_data
            }
        else:
            response_data = {
                "status": 404,
                "message": "user not found"
            }
        
        return Response(response_data)
