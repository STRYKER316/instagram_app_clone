from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from .models import UserProfile


class UserCreateSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        # fields
        fields = ('username', 'email', 'password', )

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = get_user_model().objects.create(**validated_data)

        # create user profile
        UserProfile.objects.create(user=user)

        return user
