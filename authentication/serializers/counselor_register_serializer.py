from rest_framework import serializers
from authentication.models import CounselorProfile, User
from django.db import transaction
from django.contrib.auth.password_validation import validate_password

class CounselorProfileCreateSerializer(serializers.ModelSerializer):
    counselor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = CounselorProfile
        fields = ['counselor', 'specialization', 'years_of_experience']

class CounselorRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    profile = CounselorProfileCreateSerializer(required=False)
    
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
        validated_data['role'] = 'counselor'
        user = User.objects.create_user(**validated_data)
        
        if profile_data:
            CounselorProfile.objects.create(counselor=user, **profile_data)
        return user
    
    
class CounselorProfileReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='counselor.id', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CounselorProfile
        fields = ['id', 'full_name', 'specialization', 'years_of_experience']
        
    def get_full_name(self, obj):
        first = obj.counselor.first_name or ""
        last = obj.counselor.last_name or ""
        full = f"{first} {last}".strip()
        return full or obj.counselor.username