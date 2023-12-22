from django.urls import path
from .views import *


urlpatterns = [
    path("friendRequest/", FriendRequestView.as_view(), name="friend_request"),
    path("sendRequest/", FriendRequestCreateView.as_view(), name="send_request"),
    path("friendView/", FriendListView.as_view(), name="friend_view"),
]