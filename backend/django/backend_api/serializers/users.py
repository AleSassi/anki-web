from rest_framework.serializers import ModelSerializer

from ..models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}
