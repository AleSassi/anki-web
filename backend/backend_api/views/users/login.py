from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json


class LoginAPIView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        POST API for login
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

        # authentication user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": "User has been logged in"}, status=200) # Redirect to home page
        return JsonResponse(
            {"errors": "Invalid credentials"},
            status=400,
        )
