from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField
from random import randint
from typing import List



class Game(models.Model):
    """A game object."""

    NUMBER_OF_MOVES = 12
    NUMBER_OF_HOLES = 4
    CODE_COLOR_CHOICES = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

    number_of_moves = models.PositiveSmallIntegerField()
    codebreaker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code =  JSONField()

    @staticmethod
    def generate_random_code() -> List:
        """Generate a random code with a random color from CODE_COLOR_CHOICES for each hole in NUMBER_OF_HOLES."""
        code = []
        i = 0
        while i < Game.NUMBER_OF_HOLES:
            # get random color from the games color choices and append it to the code
            code.append(Game.CODE_COLOR_CHOICES[randint(0, len(Game.CODE_COLOR_CHOICES)-1)])
            i += 1
        return code

    def get_moves_count(self) -> int:
        """Return the number of moves already played in a game."""
        return Move.objects.filter(game_id=self.id).count()

    def get_game_won(self) -> bool:
        """Return true if the game has been won and false if the game hasn't been won yet."""
        count_winning_move = Move.objects.filter(game_id=self.id, result=["black", "black", "black", "black"]).count()
        if count_winning_move > 0:
            return True
        return False

    def get_remaining_moves(self) -> int:
        """Return the number of remaining moves available in a game."""
        return self.NUMBER_OF_MOVES - self.get_moves_count()



class Move(models.Model):
    """A move object."""

    game = models.ForeignKey(Game, related_name='moves', on_delete=models.CASCADE)
    code = JSONField()
    result = JSONField()

    @staticmethod
    def get_result(game_code: List, move_code: List):
        """Return the result of a move: one black per correct hole and color, one white per incorrect hole and correct color."""
        result = []
        # create copies so original codes aren't modified
        new_game_code = game_code.copy()
        new_move_code = move_code.copy()
        # add black to results for each correct hole and correct color
        # delete any correct hole and color combinations,
            # so they aren't counted with incorrect hole and correct color combinations
        i = 0
        while i < len(new_game_code) and i < len(new_move_code):
            if new_game_code[i] == new_move_code[i]:
                result.append("black")
                del new_game_code[i]
                del new_move_code[i]
            else:
                i += 1
        # add white to results for each incorrect hole and correct color
        # remove the first instance of that color from the game code,
            # so it can only be counted once
        for color in new_move_code:
            if color in new_game_code:
                result.append("white")
                new_game_code.remove(color)
        return result
