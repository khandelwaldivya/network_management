from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from friend.views import BaseView
from rest_framework_jwt.settings import api_settings
from django.db.models import Q
from users.services import UserCreateService
from .models import User
from .serializers import ( TokenSerializer, UserLoginDataSerializer,RegisterUserSerialiers)
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class RegisterView(APIView):
    @staticmethod
    def post(request):
        payload = RegisterUserSerialiers(data=request.data)
        if payload.is_valid(raise_exception=True):
            return UserCreateService.execute(
                    {"data": payload.validated_data}
                )

# class LoginView(TokenObtainPairView):
#     serializer_class = UserLoginSerializer
#     permission_classes = (permissions.AllowAny,)
    
#     def post(self, request, *args, **kwargs):
        
#         if request.data == {}:
#             return Response({'message':'Please fill give email and password',"sucess":False})
#         if request.data.get("email")== None or request.data.get("email")== '':
#             return Response({'message':'Please Enter Your Email',"sucess":False})
#         elif request.data.get("password")== None or request.data.get("password")== '':
#             return Response({'message':'Please Enter Your password',"sucess":False})

#         self.email = request.data.get("email")
#         self.password = request.data.get("password")
#         user = authenticate(email=self.email, password=self.password)
#         if user is not None:    
#             login(request,user,backend='django.contrib.auth.backends.ModelBackend',)
#             serializer = TokenSerializer(data={"token": jwt_encode_handler(jwt_payload_handler(user))})
#             serializer.is_valid()
#             return Response({"token":serializer.data['token'],"sucess":True})
#         return Response(data={"message": "Invalid credentials","sucess":False},status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(TokenObtainPairView):
    serializer_class = UserLoginDataSerializer

    def post(self,request):
        breakpoint()
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"message": "Please provide both email and password.", "success": False}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"message": "Invalid credentials", "success": False}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = TokenSerializer(data={"token": jwt_encode_handler(jwt_payload_handler(user))})
        serializer.is_valid()

        return Response({"token": serializer.data['token'], "success": True})
    
    
class UserSearchView(BaseView):
    @staticmethod
    def get(request):
        search_keyword = request.GET.get('search', '')
        return Response(User.objects.filter(Q(email__icontains=search_keyword) | Q(full_name__icontains=search_keyword)).values("id","email","full_name"))