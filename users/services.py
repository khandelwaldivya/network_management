from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from service_objects.services import Service
from users.models import User


class UserCreateService(Service):
    def process(self):
        try:
            if User.objects.filter(email=self.data["data"]["email"]).exists():
                return Response(
                    {"Error": "Username already taken dsd."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.create(
                full_name=self.data["data"]["full_name"],
                email=self.data["data"]["email"],
            )
            user.set_password(self.data["data"]["password"])
            user.save()
            return Response(
                {"Message": "User created Successfully"}, status=status.HTTP_201_CREATED
            )
        except IntegrityError as e:
            return Response({"Error": f"Went Something Wrong {str(e)}"})