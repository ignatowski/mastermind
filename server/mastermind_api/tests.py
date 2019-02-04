from .models import Game, Move
from users.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient



class GamesTest(APITestCase):
    """Class to test game related services."""

    def setUp(self) -> None:
        """Initial set up for testing game services."""
        self.password = 'password1234'
        self.testuser1game = User.objects.create_user('testuser1game', 'testuser1game@test.com', self.password)
        self.testuser2game = User.objects.create_user('testuser2game', 'testuser2game@test.com', self.password)
        self.game1 = Game.objects.create(number_of_moves=12, codebreaker=self.testuser1game, code=["red", "orange", "yellow", "green"])
        self.user_login_url = reverse('user-login')
        self.game_create_url = reverse('game-create')
        self.game_details_url = reverse('game-details', kwargs={'pk': self.game1.id})

    def test_game_create_success(self) -> None:
        """Test that a game is able to be successfully created."""

        # user can create a game with empty body
        data = None

        login_data = {
            'username': self.testuser1game.username,
            'password': self.password
        }
        login_response = self.client.post(self.user_login_url, login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        response = self.client.post(self.game_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['number_of_moves'], 12)
        self.assertEqual(response.data['codebreaker'], self.testuser1game.id)
        self.assertTrue('id' in response.data)
        self.assertTrue('color_choices' in response.data)
        self.assertFalse('code' in response.data)

    def test_game_create_fail_not_logged_in(self) -> None:
        """Test that a game cannot be created if not logged in."""

        data = None

        response = self.client.post(self.game_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_game_create_success_not_override(self) -> None:
        """Test that a game is able to be successfully created and not override defaults."""

        # user can create a game and not override given number_of_moves, codebreaker, and code
        data = {
            'number_of_moves': 20,
            'codebreaker': 2,
            'code': [
                "red",
                "red",
                "red",
                "red"
            ]
        }

        login_data = {
            'username': self.testuser1game.username,
            'password': self.password
        }
        login_response = self.client.post(self.user_login_url, login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        response = self.client.post(self.game_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['number_of_moves'], 12)
        self.assertEqual(response.data['codebreaker'], self.testuser1game.id)
        self.assertTrue('id' in response.data)
        self.assertTrue('color_choices' in response.data)
        self.assertFalse('code' in response.data)

    def test_game_details_success(self) -> None:
        """Test that a user is able to get a game that is theirs."""

        login_data = {
            'username': self.testuser1game.username,
            'password': self.password
        }
        login_response = self.client.post(self.user_login_url, login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        response = self.client.get(self.game_details_url, pk=self.game1.id)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number_of_moves'], 12)
        self.assertEqual(response.data['codebreaker'], self.testuser1game.id)
        self.assertTrue('id' in response.data)
        self.assertTrue('color_choices' in response.data)
        self.assertTrue('moves' in response.data)
        self.assertFalse('code' in response.data)

    def test_game_details_fail_not_owner(self) -> None:
        """Test that a user is not able to get a game that is not theirs."""

        login_data = {
            'username': self.testuser2game.username,
            'password': self.password
        }
        login_response = self.client.post(self.user_login_url, login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        response = self.client.get(self.game_details_url, pk=self.game1.id)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_game_details_fail_not_logged_in(self) -> None:
        """Test that not able to get a game when not logged in."""

        response = self.client.get(self.game_details_url, pk=self.game1.id)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class MovesTest(APITestCase):
    """Class to test move related services."""

    def setUp(self) -> None:
        """Initial set up for testing move services."""
        self.password = 'password1234'
        self.testuser1game = User.objects.create_user('testuser1game', 'testuser1game@test.com', self.password)
        self.testuser2game = User.objects.create_user('testuser2game', 'testuser2game@test.com', self.password)
        self.game1 = Game.objects.create(number_of_moves=12, codebreaker=self.testuser1game, code=["red", "orange", "yellow", "green"])
        self.user_login_url = reverse('user-login')
        self.move_create_url = reverse('move-create')

    def test_move_create_success_won(self) -> None:
        """Test that moves are able to be successfully created with expected results."""

        # user can create a move, result empty list
        data = {
            "game": self.game1.id,
            "code": [
                "blue",
                "blue",
                "blue",
                "purple"
            ]
        }
        login_data = {
            'username': self.testuser1game.username,
            'password': self.password
        }
        login_response = self.client.post(self.user_login_url, login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['game'], data['game'])
        self.assertEqual(response.data['code'], data['code'])
        self.assertEqual(response.data['result'], [])

        # user can create a move, result four whites
        data = {"game": self.game1.id, "code": ["green", "red", "orange", "yellow"]}
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['game'], data['game'])
        self.assertEqual(response.data['code'], data['code'])
        self.assertEqual(response.data['result'], ["white", "white", "white", "white"])

        # user can create a move, result two whites, two blacks
        data = {"game": self.game1.id, "code": ["red", "orange", "green", "yellow"]}
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['game'], data['game'])
        self.assertEqual(response.data['code'], data['code'])
        self.assertEqual(response.data['result'], ["black", "black", "white", "white"])

        # user can create a move, result one white, one black
        data = {"game": self.game1.id, "code": ["red", "blue", "green", "blue"]}
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 4)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['game'], data['game'])
        self.assertEqual(response.data['code'], data['code'])
        self.assertEqual(response.data['result'], ["black", "white"])

        # user can create a move, result one white
        data = {"game": self.game1.id, "code": ["blue", "blue", "green", "blue"]}
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 5)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['game'], data['game'])
        self.assertEqual(response.data['code'], data['code'])
        self.assertEqual(response.data['result'], ["white"])

        # user can create a move, result one black
        data = {"game": self.game1.id, "code": ["red", "blue", "blue", "blue"]}
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 6)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['game'], data['game'])
        self.assertEqual(response.data['code'], data['code'])
        self.assertEqual(response.data['result'], ["black"])

        # user can create a move, result four blacks
        data = {"game": self.game1.id, "code": ["red", "orange", "yellow", "green"]}
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 7)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['game'], data['game'])
        self.assertEqual(response.data['code'], data['code'])
        self.assertEqual(response.data['result'], ["black", "black", "black", "black"])

        # user cannot create a move, result already won
        data = {"game": self.game1.id, "code": ["red", "orange", "yellow", "green"]}
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 7)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_move_create_success_lost(self) -> None:
        """Test that moves are able to be successfully created with expected results."""

        # user only has n number of moves
        data = {
            "game": self.game1.id,
            "code": [
                "blue",
                "blue",
                "blue",
                "purple"
            ]
        }
        login_data = {
            'username': self.testuser1game.username,
            'password': self.password
        }
        login_response = self.client.post(self.user_login_url, login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        i = 0
        while i < Game.NUMBER_OF_MOVES:
            response = self.client.post(self.move_create_url, data, format='json')
            self.assertEqual(Game.objects.count(), 1)
            self.assertEqual(Move.objects.count(), i+1)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['game'], data['game'])
            self.assertEqual(response.data['code'], data['code'])
            self.assertEqual(response.data['result'], [])
            i += 1
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), Game.NUMBER_OF_MOVES)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_move_create_fail_not_owner(self) -> None:
        """Test that user cannot make moves on game that isn't theirs."""

        data = {
            "game": self.game1.id,
            "code": [
                "blue",
                "blue",
                "blue",
                "purple"
            ]
        }
        login_data = {
            'username': self.testuser2game.username,
            'password': self.password
        }
        login_response = self.client.post(self.user_login_url, login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_move_create_fail_not_logged_in(self) -> None:
        """Test that cannot make move when not logged in"""

        data = {
            "game": self.game1.id,
            "code": [
                "blue",
                "blue",
                "blue",
                "purple"
            ]
        }
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_move_create_fail_less_holes(self) -> None:
        """Test that user cannot make a move with less holes"""

        data = {
            "game": self.game1.id,
            "code": [
                "blue",
                "blue",
                "blue"
            ]
        }
        login_data = {
            'username': self.testuser1game.username,
            'password': self.password
        }
        login_response = self.client.post(self.user_login_url, login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_move_create_fail_more_holes(self) -> None:
        """Test that user cannot make a move with more holes"""

        data = {
            "game": self.game1.id,
            "code": [
                "blue",
                "blue",
                "blue",
                "blue",
                "blue"
            ]
        }
        login_data = {
            'username': self.testuser1game.username,
            'password': self.password
        }
        login_response = self.client.post(self.user_login_url, login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_move_create_fail_code_choice_invalid(self) -> None:
        """Test that user cannot make a move with an invalid code choice"""

        data = {
            "game": self.game1.id,
            "code": [
                "blue",
                "blue",
                "blue",
                "pink"
            ]
        }
        login_data = {
            'username': self.testuser1game.username,
            'password': self.password
        }
        login_response = self.client.post(self.user_login_url, login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_move_create_fail_code_game_empty(self) -> None:
        """Test that user cannot make a move without a game id"""

        data = {
            "game": None,
            "code": [
                "blue",
                "blue",
                "blue",
                "blue"
            ]
        }
        login_data = {
            'username': self.testuser1game.username,
            'password': self.password
        }
        login_response = self.client.post(self.user_login_url, login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_move_create_fail_code_code_empty(self) -> None:
        """Test that user cannot make a move without a code"""

        data = {
            "game": self.game1.id,
            "code": None
        }
        login_data = {
            'username': self.testuser1game.username,
            'password': self.password
        }
        login_response = self.client.post(self.user_login_url, login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_move_create_fail_code_node_list(self) -> None:
        """Test that user cannot make a move without a code"""

        data = {
            "game": self.game1.id,
            "code": "code"
        }
        login_data = {
            'username': self.testuser1game.username,
            'password': self.password
        }
        login_response = self.client.post(self.user_login_url, login_data, format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + login_response.data['token'])
        response = self.client.post(self.move_create_url, data, format='json')
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Move.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
