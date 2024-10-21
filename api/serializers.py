from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Content


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        ) 

        return user
    

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'user', 'name', 'phone_number', 'alternate_phone_number', 'profile_image']
        read_only_fields = ['user']