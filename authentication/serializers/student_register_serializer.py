from rest_framework import serializers
from authentication.models import User, StudentProfile
from django.db import transaction
from career.models import Career
from django.contrib.auth.password_validation import validate_password



class StudentProfileSerializer(serializers.ModelSerializer):
    """Nested profile — used inside StudentSerializer and StudentRegisterSerializer"""
    career = serializers.PrimaryKeyRelatedField(
        queryset=Career.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = StudentProfile
        fields = [
            'education_level', 'preferred_learning_mode', 'career',
            'bio', 'address', 'birth_date'
        ]


class StudentRegisterSerializer(serializers.ModelSerializer):
    """Write-only serializer for new student registration"""
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    profile = StudentProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'phone', 
                  'last_name', 'password', 'password2', 'profile']
        read_only_fields=['id']

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
        validated_data['role'] = 'student'
        
        user = User.objects.create_user(**validated_data)
        
        if profile_data is not None:
            StudentProfile.objects.create(student=user, **profile_data)
        
        return user


class StudentUpdateSerializer(serializers.ModelSerializer):
    """Read-update serializer for existing students"""
    profile = StudentProfileSerializer(source='student_profile', required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'phone', 'profile']
        read_only_fields = ['id', 'username']
    
    @transaction.atomic
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('student_profile', None)
        
        instance = super().update(instance, validated_data)
        
        if profile_data is not None:
            StudentProfile.objects.update_or_create(
                student=instance,
                defaults=profile_data
            )
        
        return instance


class StudentUserMiniSerializer(serializers.ModelSerializer):
    """Lightweight read-only serializer for listings"""
    education_level = serializers.SerializerMethodField()
    preferred_learning_mode = serializers.SerializerMethodField()
    career = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 
                  'education_level', 'preferred_learning_mode', 'career']
    
    def _get_profile(self, obj):
        return getattr(obj, 'student_profile', None)
    
    def get_education_level(self, obj):
        profile = self._get_profile(obj)
        return profile.education_level if profile else None
    
    def get_preferred_learning_mode(self, obj):
        profile = self._get_profile(obj)
        return profile.preferred_learning_mode if profile else None
    
    def get_career(self, obj):
        profile = self._get_profile(obj)
        return profile.career.title if profile and profile.career else None