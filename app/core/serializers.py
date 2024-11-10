"""
Serializers for the Core API
"""
from django.contrib.auth import (
    get_user_model,
    authenticate
)
from core import models
from django.utils.translation import gettext as _
from rest_framework import serializers
from core.utils import generate_unique_pin


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Validates and authenticated users"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticated with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
        }

        def create(self, validated_data):
            """Create and return a user with encrypted password"""
            return get_user_model().objects.create_user(**validated_data)

        def update(self, instance, validated_data):
            """Update and return user"""
            password = validated_data.pop('password', None)
            user = super().update(instance, validated_data)

            if password:
                user.set_password(password)
                user.save()
            return user


class PINGenerateRequestSerializer(serializers.Serializer):
    pin_count = serializers.IntegerField(min_value=1)
    pin_type = serializers.ChoiceField(
        choices=[('teacher', 'Teacher'),('student', 'Student')]
    )


class PINSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PIN
        fields = ['id', 'pin_code', 'pin_type', 'is_used', 'used_by']
        read_only_fields = ('id',)
