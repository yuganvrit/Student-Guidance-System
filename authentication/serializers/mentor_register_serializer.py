from rest_framework import serializers
from authentication.models import User, MentorProfile
from django.contrib.auth.password_validation import validate_password
from skill.models import Skill  
from django.db import transaction


class MentorProfileCreateSerializer(serializers.ModelSerializer):   
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True, required=False)
    class Meta:
        model = MentorProfile
        fields = ['expertise_area', 'years_of_experience', 'skills']

class MentorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    profile = MentorProfileCreateSerializer(required=False)
    class Meta:
        model = User
        fields = ['username', 'email','first_name','phone','last_name', 'password', 'password2', 'profile']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        validate_password(attrs['password'])
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        validated_data.pop('password2')
        validated_data['role'] = 'mentor'
        
        user = User.objects.create_user(**validated_data)
        
        if profile_data:
            skills = profile_data.pop('skills', [])
            mentor_profile = MentorProfile.objects.create(mentor=user, **profile_data)
            if skills:
                mentor_profile.skills.set(skills)
        
        return user