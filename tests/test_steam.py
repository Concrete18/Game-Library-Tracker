import pytest
import requests

# classes
from classes.steam import Steam
from classes.utils import get_steam_api_key_and_id


class TestGetOwnedSteamGames:

    @pytest.fixture
    def mock_response(self, mocker):
        # Create a mock response object
        mock_response = mocker.Mock()
        # Set the JSON data for the response
        mock_response.json.return_value = {
            "response": {
                "games": [
                    {"name": "Game 1", "appid": 123},
                    {"name": "Game 2", "appid": 456},
                ]
            }
        }
        # Set the status code and whether the request was successful
        mock_response.ok = True
        return mock_response

    def test_get_owned_steam_games_success(self, mock_response, mocker):
        steam = Steam()
        steam_key, steam_id = get_steam_api_key_and_id()
        # Mock requests.get and return the mock response
        mocker.patch("requests.get", return_value=mock_response)
        # Call the function you want to test
        result = steam.get_owned_steam_games(steam_key, steam_id)
        # Assert that the function returns the expected result
        assert result == [
            {"name": "Game 1", "appid": 123},
            {"name": "Game 2", "appid": 456},
        ]

    def test_get_owned_steam_games_request_error(self, mocker):
        # Create an instance of YourClass
        steam = Steam()
        steam_key, _ = get_steam_api_key_and_id()
        # Mock requests.get to raise an exception
        mocker.patch(
            "requests.get", side_effect=requests.RequestException("Test error")
        )
        # Call the function you want to test
        result = steam.get_owned_steam_games(steam_key, 123456)
        # Assert that the function returns None
        assert result is None


class TestSteamReview:
    """
    Tests `get_steam_review`. Due to changing reviews, it only tests for acquiring
    floats for percent and integers for total.
    """

    def test_get_owned_steam_games_success(self):
        steam = Steam()

        # TODO mock request
        percent, total = steam.get_steam_review(app_id=752590)
        assert isinstance(percent, float)
        assert isinstance(total, int)


class TestGetRecentlyPlayedGames:
    @pytest.fixture
    def mock_response(self, mocker):
        # Create a mock response object
        mock_response = mocker.Mock()
        # Set the JSON data for the response
        mock_response.json.return_value = {
            "response": {
                "games": [
                    {"name": "Game 1", "appid": 123, "playtime_forever": 10},
                    {"name": "Game 2", "appid": 456, "playtime_forever": 20},
                ]
            }
        }
        # Set the status code and whether the request was successful
        mock_response.ok = True
        return mock_response

    def test_get_recently_played_steam_games_success(self, mock_response, mocker):
        steam = Steam()
        steam_key, steam_id = get_steam_api_key_and_id()

        mocker.patch("requests.get", return_value=mock_response)

        # TODO mock request
        result = steam.get_recently_played_steam_games(
            steam_key,
            steam_id,
            game_count=1,
        )

        assert result == [
            {"name": "Game 1", "appid": 123, "playtime_forever": 10},
            {"name": "Game 2", "appid": 456, "playtime_forever": 20},
        ]

    def test_get_recently_played_steam_games_request_error(self, mocker):
        # Create an instance of YourClass
        steam = Steam()
        steam_key, _ = get_steam_api_key_and_id()
        # Mock requests.get to raise an exception
        mocker.patch(
            "requests.get", side_effect=requests.RequestException("Test error")
        )
        # Call the function you want to test
        result = steam.get_recently_played_steam_games(steam_key, 123456)
        # Assert that the function returns None
        assert result is None


class TestGetSteamGamePlayerCount:
    steam = Steam()
    steam_key, _ = get_steam_api_key_and_id()

    def test_get_steam_game_player_count(self):
        """
        Tests `get_steam_game_player_count` function.
        """
        # TODO mock request
        app_id = 730
        player_count = self.steam.get_steam_game_player_count(app_id, self.steam_key)
        assert isinstance(player_count, int)


class TestGetAppList:
    steam = Steam()

    def test_get_app_list(self):
        """
        Tests `get_game_info` function.
        """
        # TODO mock request
        app_list = self.steam.get_app_list()
        assert isinstance(app_list[0]["appid"], int)
        assert isinstance(app_list[0]["name"], str)


class TestGetAppId:
    steam = Steam()

    app_list = [{"appid": 12345, "name": "Hades"}]

    def test_get_app_id(self):
        app_id = self.steam.get_app_id("Hades", self.app_list)
        assert app_id == 12345

    def test_app_id_not_found(self):
        app_id = self.steam.get_app_id("Not Real", self.app_list)
        assert app_id == None


if __name__ == "__main__":
    pytest.main([__file__])
