from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from rest_framework.response import Response
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = super(UserSerializer, self).create(validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user
        except Exception as e:
            error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError({'errors': error})


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

# class MyUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('email',)

#         def create(self, validated_data):
#             user = User.objects.create_user(**validated_data)
#             return user
