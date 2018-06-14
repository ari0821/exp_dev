from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from .models import ExpUser, ExpUserManager


class ExpUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = ExpUser
        fields = ('id', 'username', 'email', 'profile', 'password')

    def create(self, validated_data):
        return ExpUser.objects.create_user(request_data=validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        else:
            instance = super().update(instance, validated_data)
        instance.save()
        return instance
