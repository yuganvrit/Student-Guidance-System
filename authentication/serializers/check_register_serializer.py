from rest_framework import serializers
from authentication.models import User

class Register_serializer(serializers.Serializer):
    password = serializers.CharField(max_length=100)
    password2=serializers.CharField(max_length=100)

    class Meta:
        fields = ['id', 'username', 'email','first_name', 'last_name', 'phone', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Passwords do not match')
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.all_objects.create(**validated_data)
        return user

    def to_representation(self, instance):
        return {
            'user_id':instance.id,
            'username':instance.username,
            'email':instance.email,
            'message':'User Created Successfully.'
        }