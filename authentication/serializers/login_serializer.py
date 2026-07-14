from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)


    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            email=attrs['email'],
            password = attrs['password']
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        
        
        
        attrs['user'] = user
        return attrs
