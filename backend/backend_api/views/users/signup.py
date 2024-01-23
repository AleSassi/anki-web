from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json
from ...models import User


class SignupAPIView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        POST API for signup
        """
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        if username is None:
            return JsonResponse(
                {"errors": {"detail": "Please enter username"}}, status=400
            )
        elif password is None:
            return JsonResponse(
                {"errors": {"detail": "Please enter password"}}, status=400
            )
        elif len(password) < 8:
            return JsonResponse(
                {"errors": "Password must be >= 8 characters long"}, status=400
            )

        # create user
        user = self.create_user(username=username, password=password)

        if user is not None:
            return JsonResponse({"success": "User created"}, status=200) # Redirect to login
        return JsonResponse(
            {"errors": "Operation failed"},
            status=400,
        )

    def create_user(self, username: str, password: str):
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user
