from rest_framework.authentication import BaseAuthentication
from auth_api import exceptions
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import credentials, auth, firestore
from django.conf import settings

# FirebaseAuthenticaiton
class FirebaseAuthentication(BaseAuthentication):
    """override authenticate method and write our custom firebase authentication."""
    def authenticate(self, request):
        """Get the authorization Token, It raise exception when no authorization Token is given"""
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise exceptions.NoAuthToken("No auth token provided")
        
        """Decoding the Token. It raise exception when decode failed."""
        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.InvalidAuthToken("Invalid auth token")
        
        if not id_token or not decoded_token:
            raise exceptions.InvalidAuthToken("Invalid auth token")
        
        """Get the uid of an user"""
        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise exceptions.FirebaseError()
    
        db = firestore.client()
        user_ref = db.collection('users').document(uid)
        user = user_ref.get()
        
        if not user.exists:
            user_ref.set({"username": uid})

        """Get or create the user"""
        user, created = User.objects.get_or_create(username=uid)
        return (user, None)