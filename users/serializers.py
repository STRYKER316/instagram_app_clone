from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import UserProfile


class UserCreateSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', )

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = get_user_model().objects.create(**validated_data)

        # create user profile
        UserProfile.objects.create(user=user)

        return user


class UserViewSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name')


class UserProfileViewSerializer(ModelSerializer):

    user = UserViewSerializer()

    class Meta:
        model = UserProfile
        # fields = ('bio', 'profile_pic_url', 'user', 'created_on', 'updated_on')
        exclude = ('id', 'is_verified')


class UserProfileUpdateSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = ('bio', 'first_name', 'last_name', 'profile_pic_url', )

    def update(self, instance, validated_data):
        user = instance.user

        user.first_name = validated_data.pop('first_name', user.first_name)
        user.last_name = validated_data.pop('last_name', user.last_name)
        user.save()

        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_pic_url = validated_data.get('profile_pic_url', instance.profile_pic_url)
        instance.save()

        return instance
