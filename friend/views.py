from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from friend.models import Friendship
from friend.serializers import FriendshipListSerializer, FriendshipSerializer
from rest_framework import generics,status
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from rest_framework.views import APIView
from users.models import User


class BaseView(APIView):
    permission_classes = [IsAuthenticated]

class FriendRequestView(BaseView):
    @staticmethod
    def get(self):
        return FriendshipListSerializer(Friendship.objects.filter(to_user=self.request.user, status='pending')).data

class FriendRequestCreateView(BaseView):
    @ratelimit(key='user', rate='3/m', block=True)
    @staticmethod
    def post(request):
        payload = FriendshipSerializer(data=request.data)
        if payload.is_valid(raise_exceptions = True):
            try:
                Friendship.objects.create(from_user=request.user, status='Pending',to_user=User.objects.get(id=payload.validated_data.get("to_user")))
                return Response({"Message":"Request send SuccessFully."})
            except User.DoesNotExist:
                return Response({"Message":"Invalid User."})

class FriendListView(BaseView):
    @staticmethod
    def get(self):
        return FriendshipListSerializer(Friendship.objects.filter(from_user=self.request.user, status='Accepted')).data