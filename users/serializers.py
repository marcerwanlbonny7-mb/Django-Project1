from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone', 'region', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['role'] = 'CLIENT'
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['adresse', 'photo']


class AgentPresenceSerializer(serializers.ModelSerializer):
    nom = serializers.CharField(source='username', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'nom', 'is_online', 'last_seen']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'region', 'role', 'is_online', 'last_seen', 'created_at', 'profile']
        read_only_fields = ['id', 'role', 'is_online', 'last_seen', 'created_at']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if profile_data:
            profile, _ = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        return instance
