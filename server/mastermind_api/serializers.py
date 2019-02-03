from mastermind_api.models import Game, Move
from rest_framework import serializers
from users.models import User
from typing import List



class GameCreateSerializer(serializers.ModelSerializer):
    """Serializer to handle game creation."""

    number_of_moves = serializers.IntegerField(required=False, default='default_number_of_moves')
    codebreaker = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    code = serializers.JSONField(required=False, default='default_code', write_only=True)

    def default_number_of_moves(self) -> int:
        return Game.NUMBER_OF_MOVES

    def default_code(self) -> List:
        return Game.generate_random_code()

    def validate_number_of_moves(self, value: int) -> int:
        return self.default_number_of_moves()

    def validate_code(self, value: List) -> List:
        return self.default_code()

    class Meta:
        model = Game
        fields = ('id', 'number_of_moves', 'codebreaker', 'code')



class MoveCreateSerializer(serializers.ModelSerializer):
    """Serializer to handle move creation."""

    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all(), required=True)
    code = serializers.JSONField(required=True)
    result = serializers.JSONField(required=False)

    def validate(self, data: List) -> List:
        # check that the provided code is a list,
            # that it has the correct number of color guesses to fill each hole,
            # and that the color guesses are valid color choices
        if not isinstance(data['code'], list):
            raise serializers.ValidationError("Code must be a json array.")
        if len(data['code']) != Game.NUMBER_OF_HOLES:
            raise serializers.ValidationError("Code must be " + str(Game.NUMBER_OF_HOLES) + " colors.")
        for color in data['code']:
            if color not in Game.CODE_COLOR_CHOICES:
                raise serializers.ValidationError("Color must be one of " + str(Game.CODE_COLOR_CHOICES))
        # Check that the game has not already been won,
            # and that the game has remaining moves
        if data['game'].get_game_won() == True:
            raise serializers.ValidationError("Game already won.")
        if data['game'].get_remaining_moves() <= 0:
            raise serializers.ValidationError("No remaining moves left.")
        # calculate the result of the move
        data['result'] = Move.get_result(data['game'].code, data['code'])
        return data

    class Meta:
        model = Move
        fields = ('id', 'game', 'code', 'result')



class MoveDetailsSerializer(serializers.ModelSerializer):
    """Serializer to handle getting a move."""

    class Meta:
        model = Move
        fields = ('id', 'game', 'code', 'result')



class GameDetailsSerializer(serializers.ModelSerializer):
    """Serializer to handle getting a game with move history."""

    moves = MoveDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'number_of_moves', 'codebreaker', 'moves')
