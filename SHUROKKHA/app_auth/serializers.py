from rest_framework import serializers
from .models import AppUser
from django.contrib.auth.hashers import make_password

class AppUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = '__all__'




    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
