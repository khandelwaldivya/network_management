from rest_framework import serializers
from friend.models import Friendship
from users.serializers import UserListSerializer

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ('from_user', 'to_user', 'status')
        
class FriendshipListSerializer(serializers.ModelSerializer):
    to_user = UserListSerializer()
    class Meta:
        model = Friendship
        fields = ("id",'from_user', 'to_user', 'status')