from rest_framework import serializers
from rest_framework.generics import ListAPIView

from app.authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class UserAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
