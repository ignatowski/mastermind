from mastermind_api.models import Game
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mastermind_api.serializers import GameCreateSerializer, GameDetailsSerializer, MoveCreateSerializer
from rest_framework import permissions
from mastermind_api.permissions import IsCodebreaker
from typing import Dict



class GameCreate(APIView):
    """Class to handle game creation."""

    # user must be logged in to create a game
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request: Dict, format: str='json') -> Response:
        """Create a new game."""
        # set the game's codebreaker based on the logged in user's id
        request.data['codebreaker'] = request.user.id
        # serialize the request body
        serializer = GameCreateSerializer(data=request.data)
        # check that the request data was valid
            # this actually ignores all user input and creates a game with a random code
        if serializer.is_valid():
            # save the new Game object to the database
            game = serializer.save()
            # check that the game was saved correctly to the database
            if game:
                json = serializer.data
                # append the color choies to the results,
                    # so the user knows which options they have for a move
                json['color_choices'] = Game.CODE_COLOR_CHOICES
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GameDetails(APIView):
    """Class to get game details with move history."""

    # user must be logged in and own a game to get it
    permission_classes = (permissions.IsAuthenticated, IsCodebreaker,)

    def get(self, request: Dict, pk: int) -> Response:
        # get the game object by its primary key
        game = Game.objects.get(pk=pk)
        # check that the user is the codebreaker of the game
        self.check_object_permissions(self.request, game)
        # serialize the game object
        serializer = GameDetailsSerializer(game)
        json = serializer.data
        # append the color choies to the results,
            # so the user knows which options they have for a move
        json['color_choices'] = Game.CODE_COLOR_CHOICES
        return Response(json, status=status.HTTP_200_OK)



class MoveCreate(APIView):
    """Class to create a move for a given game."""

    # user must be logged in and own a game to create a move for it
    permission_classes = (permissions.IsAuthenticated, IsCodebreaker,)

    def post(self, request: Dict, format: str='json') -> Response:
        # serialize the request body
        serializer = MoveCreateSerializer(data=request.data)
        # check that the request data was valid
            # and calculate the result of their code guess
        if serializer.is_valid():
            # check that the user is the codebreaker of the game
            self.check_object_permissions(self.request, serializer.validated_data['game'])
            # save the new Move object to the database
            move = serializer.save()
            # check that the move was saved correctly to the database
            if move:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
