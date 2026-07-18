from rest_framework import serializers
from authentication.models import User, StudentProfile
from django.db import transaction
from career.models import Career
from django.contrib.auth.password_validation import validate_password

class StudentProfileCreateSerializer(serializers.ModelSerializer):
    career = serializers.PrimaryKeyRelatedField(queryset=Career.objects.all(), required=False, allow_null=True)
    class Meta:
        model = StudentProfile
        fields = ['education_level', 'preferred_learning_mode', 'career']

class StudentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    profile = StudentProfileCreateSerializer(required=False)
    
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
        validated_data['role'] = 'student'
        user = User.objects.create_user(**validated_data)
        
        if profile_data:
            StudentProfile.objects.create(student=user, **profile_data)
        return user
    
    
class StudentProfileReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='student.id', read_only=True)
    full_name = serializers.SerializerMethodField()
    career = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'full_name', 'education_level', 'preferred_learning_mode', 'career']
        
    def get_full_name(self, obj):
        first = obj.student.first_name or ""
        last = obj.student.last_name or ""
        full = f"{first} {last}".strip()
        return full or obj.student.username