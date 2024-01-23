from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.contrib.auth import logout
from django.http import JsonResponse
import json


class LogoutAPIView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        POST API for logout
        """
        logout(request=request)
        return JsonResponse({"message": "Logout successful"}, status=200) # redirect to login
