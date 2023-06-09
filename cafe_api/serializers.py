from rest_framework import serializers
from .models import Cafe, Favorite
class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = '__all__'