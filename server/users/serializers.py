from .models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from typing import Dict



class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer to handle user registration."""

    username = serializers.CharField(min_length=4, max_length=32, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True, max_length=32, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, max_length=32, write_only=True)

    def create(self, validated_data: Dict) -> User:
        """Create a new user object with the validated user registration data."""
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')



class UserLoginSerializer(serializers.Serializer):
    """Serializer to handle user login."""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    default_error_messages = {
        'inactive_account': 'User account is disabled.',
        'invalid_credentials': 'Unable to login with provided credentials.'
    }

    def __init__(self, *args, **kwargs) -> None:
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, data: Dict) -> Dict:
        # log the user in
        self.user = authenticate(username=data.get("username"), password=data.get('password'))
        if self.user:
            # if the user is deactivated throw an exception
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return data
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])
