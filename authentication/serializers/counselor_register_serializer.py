# authentication/serializers/counselor_serializer.py
from rest_framework import serializers
from authentication.models import User, CounselorProfile
from django.db import transaction
from django.contrib.auth.password_validation import validate_password


class CounselorProfileSerializer(serializers.ModelSerializer):
    """Nested profile — used inside CounselorSerializer and CounselorRegisterSerializer"""
    
    class Meta:
        model = CounselorProfile
        fields = [
            'specialization', 'years_of_experience',
            'bio', 'image', 'address', 'birth_date'
        ]


class CounselorRegisterSerializer(serializers.ModelSerializer):
    """Write-only serializer for new counselor registration"""
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    profile = CounselorProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'phone',
                  'last_name', 'password', 'password2', 'profile']
        read_only_fields = ['id']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        if password != password2:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        validate_password(password)
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        validated_data.pop('password2')
        validated_data['role'] = 'counselor'
        
        user = User.objects.create_user(**validated_data)
        
        if profile_data is not None:
            CounselorProfile.objects.create(counselor=user, **profile_data)
        
        return user


class CounselorUpdateSerializer(serializers.ModelSerializer):
    """Read-update serializer for existing counselors"""
    profile = CounselorProfileSerializer(source='counselor_profile', required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'phone', 'profile']
        read_only_fields = ['id', 'username']
    
    @transaction.atomic
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('counselor_profile', None)
        
        instance = super().update(instance, validated_data)
        
        if profile_data is not None:
            CounselorProfile.objects.update_or_create(
                counselor=instance,
                defaults=profile_data
            )
        
        return instance


class CounselorUserMiniSerializer(serializers.ModelSerializer):
    """Lightweight read-only serializer for listings"""
    full_name = serializers.SerializerMethodField()
    specialization = serializers.SerializerMethodField()
    years_of_experience = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name',
                  'specialization', 'years_of_experience']
    
    def _get_profile(self, obj):
        return getattr(obj, 'counselor_profile', None)
    
    def get_full_name(self, obj):
        first = obj.first_name or ""
        last = obj.last_name or ""
        return f"{first} {last}".strip() or obj.username
    
    def get_specialization(self, obj):
        profile = self._get_profile(obj)
        return profile.specialization if profile else None
    
    def get_years_of_experience(self, obj):
        profile = self._get_profile(obj)
        return profile.years_of_experience if profile else None