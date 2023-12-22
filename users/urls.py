from django.urls import path
from .views import *


urlpatterns = [
    path("createUser/", RegisterView.as_view(), name="user_create"),
    path("userLogin/", LoginView.as_view(), name="user_login"),
    path("userSearch/", UserSearchView.as_view(), name="user_search"),

]