from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework.authtoken.models import Token
from typing import Dict



class UserRegister(APIView):
    """Class to handle user registration."""

    def post(self, request: Dict, format: str='json') -> Response:
        """Create a new user."""
        # serialize the request body
        serializer = UserRegisterSerializer(data=request.data)
        # check that the request data was valid
        if serializer.is_valid():
            # save the new User object to the database
            user = serializer.save()
            # check that the user was saved correctly to the database
            if user:
                # generate the user's auth token
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLogin(APIView):
    """Class to handle user login."""

    def post(self, request: Dict, format: str='json') -> Response:
        """Login user."""
        # serialize the request body
        serializer = UserLoginSerializer(data=request.data)
        # check that the request data was valid
        if serializer.is_valid():
            # get the logged in user
            user = serializer.user
            if user:
                # get the user's existing auth token or generate a new one
                token, _ = Token.objects.get_or_create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
