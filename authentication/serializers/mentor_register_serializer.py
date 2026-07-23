# authentication/serializers/mentor_serializer.py
from rest_framework import serializers
from authentication.models import User, MentorProfile
from django.contrib.auth.password_validation import validate_password
from skill.models import Skill
from django.db import transaction


class MentorProfileSerializer(serializers.ModelSerializer):
    """Nested profile — used inside MentorSerializer and MentorRegisterSerializer"""
    skills = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = MentorProfile
        fields = [
            'expertise_area', 'years_of_experience', 'skills',
            'bio', 'image', 'address', 'birth_date'
        ]


class MentorRegisterSerializer(serializers.ModelSerializer):
    """Write-only serializer for new mentor registration"""
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    profile = MentorProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'phone',
                  'last_name', 'password', 'password2', 'profile']
        read_only_fields = ['id']

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        
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
        validated_data['role'] = 'mentor'
        
        user = User.objects.create_user(**validated_data)
        
        if profile_data is not None:
            skills = profile_data.pop('skills', [])
            mentor_profile = MentorProfile.objects.create(mentor=user, **profile_data)
            if skills:
                mentor_profile.skills.set(skills)
        
        return user


class MentorUpdateSerializer(serializers.ModelSerializer):
    """Read-update serializer for existing mentors"""
    profile = MentorProfileSerializer(source='mentor_profile', required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'phone', 'profile']
        read_only_fields = ['id', 'username']
    
    @transaction.atomic
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('mentor_profile', None)
        
        instance = super().update(instance, validated_data)
        
        if profile_data is not None:
            skills = profile_data.pop('skills', None)
            mentor_profile, created = MentorProfile.objects.update_or_create(
                mentor=instance,
                defaults=profile_data
            )
            if skills is not None:
                mentor_profile.skills.set(skills)
        
        return instance


class MentorUserMiniSerializer(serializers.ModelSerializer):
    """Lightweight read-only serializer for listings"""

    expertise_area = serializers.SerializerMethodField()
    years_of_experience = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name',
                  'expertise_area', 'years_of_experience', 'skills']
    
    def _get_profile(self, obj):
        return getattr(obj, 'mentor_profile', None)
    
    def get_expertise_area(self, obj):
        profile = self._get_profile(obj)
        return profile.expertise_area if profile else None
    
    def get_years_of_experience(self, obj):
        profile = self._get_profile(obj)
        return profile.years_of_experience if profile else None
    
    def get_skills(self, obj):
        profile = self._get_profile(obj)
        if profile:
            return [skill.name for skill in profile.skills.all()]
        return []