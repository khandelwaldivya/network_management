from django.db.models import fields
from rest_framework import serializers
from .models import User


class RegisterUserSerialiers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields =['email',"full_name","password"]
        

class UserLoginDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']

class TokenSerializer(serializers.Serializer):

    token = serializers.CharField(max_length=255)
    
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')
