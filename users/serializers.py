from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validated_data.get('role', 'customer').lower() == 'admin':
            validated_data['role'] = 'customer'

        try:
            validate_password(validated_data['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role')
        )
        return user
