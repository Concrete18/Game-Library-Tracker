import unittest, json

# classes
from main import Tracker


class GetYear(unittest.TestCase):
    def setUp(self):
        self.t = Tracker()

    def test_valid(self):
        date_tests = {
            "Sep 14, 2016": "2016",
            "25 Apr, 1991": "1991",
            "16 Nov, 2009": "2009",
            "Mai 25, 1991": "1991",
            "Apr , 2015": "2015",
        }
        for date, bool in date_tests.items():
            with self.subTest(date=date):
                result = self.t.get_year(date)
                self.assertEqual(result, bool)

    def test_invalid(self):
        result = self.t.get_year("this is not a date")
        self.assertEqual(result, "Invalid Date")


class GetAppId(unittest.TestCase):
    def setUp(self):
        self.t = Tracker()

    def test_get_appid(self):
        appid_tests = {
            "Inscryption": 1092790,
            "Dishonored 2": 403640,
            "Deep Rock Galactic": 548430,
        }
        for name, answer in appid_tests.items():
            with self.subTest(name=name, answer=answer):
                result = self.t.get_appid(name)
                self.assertEqual(result, answer)


class GetMetacritic(unittest.TestCase):
    def setUp(self):
        self.t = Tracker()

    def test_get_metacritic(self):
        metacritic_tests = {
            "Dishonored 2": 86,
            "Deep Rock Galactic": 85,
            "Inscryption": 85,
            "Not a Real Game": "Page Error",
        }
        for name, answer in metacritic_tests.items():
            with self.subTest(name=name, answer=answer):
                result = self.t.get_metacritic(name, "pc")
                self.assertEqual(result, answer)


class GetTimeToBeat(unittest.TestCase):
    def setUp(self):
        self.t = Tracker()

    def test_get_time_to_beat(self):
        time_to_beat_tests = [
            "Dishonored 2",
            "Deep Rock Galactic",
            "Inscryption",
        ]
        for name in time_to_beat_tests:
            with self.subTest(name=name):
                result = self.t.get_time_to_beat(name)
                self.assertIsInstance(result, float)
        result = self.t.get_time_to_beat("Not a Real Game")
        self.assertEqual(result, "Not Found")


class SteamDeckCompatability(unittest.TestCase):
    def setUp(self):
        self.t = Tracker()

    def test_valid(self):
        passes = [
            "VERIFIED",
            "PLAYABLE",
            "UNSUPPORTED",
            "UNKNOWN",
        ]
        appids = [1145360, 1167630, 667970, 1579380]
        for appid in appids:
            with self.subTest(appid=appid):
                result = self.t.steam_deck_compat(appid)
                self.assertIn(result, passes)

    def test_invalid(self):
        invalid_appid = 9**30
        self.assertFalse(self.t.steam_deck_compat(invalid_appid))


class GetStoreLink(unittest.TestCase):
    def setUp(self):
        self.t = Tracker()

    def test_get_store_link(self):
        store_link_tests = {
            "752590": "https://store.steampowered.com/app/752590/",
            "629730": "https://store.steampowered.com/app/629730/",
        }
        for appid, answer in store_link_tests.items():
            self.assertEqual(self.t.get_store_link(appid), answer)
            # tests that the url exists
            response = self.t.request_url(answer)
            self.assertIn(appid, response.url)
            self.assertTrue(response)
        # test for broken link that redirects due to app id not being found
        invalid_url = "https://store.steampowered.com/app/6546546545465484213211545730/"
        response = self.t.request_url(invalid_url)
        self.assertNotIn("6546546545465484213211545730", response.url)


class SteamReview(unittest.TestCase):
    """
    Tests get_steam_review. Due to changing reviews, it only tests for aquiring
    floats for percent and integers for total.
    """

    def setUp(self):
        self.t = Tracker()

    def test_get_steam_review(self):
        steam_review_tests = [
            752590,
            1161580,
            230410,
        ]
        for appid in steam_review_tests:
            percent, total = self.t.get_steam_review(appid=appid)
            self.assertIsInstance(percent, float)
            self.assertIsInstance(total, int)


class GetGameInfo(unittest.TestCase):
    """
    Tests get_game_info function.
    """

    def setUp(self):
        self.t = Tracker()

    def test_has_keys(self):
        """
        Checks for keys in the get_game_info result dict.
        """
        keys = [
            self.t.dev_col,
            self.t.pub_col,
            self.t.genre_col,
            self.t.ea_col,
            self.t.metacritic_col,
            self.t.steam_rev_per_col,
            self.t.steam_rev_total_col,
            self.t.release_col,
            "price",
            "discount",
            "on_sale",
            "linux_compat",
            "drm_notice",
            "categories",
            "ext_user_account_notice",
        ]
        dict = self.t.get_game_info(1145360)
        for key in keys:
            self.assertIn(key, dict.keys())

    def test_valid_types(self):
        """
        Tests get_game_info function for specific types of results.
        """
        game_info = self.t.get_game_info(appid=752590)
        self.assertIsInstance(game_info, dict)
        self.assertIsInstance(game_info["Developers"], str)
        self.assertIsInstance(game_info["Publishers"], str)
        self.assertIsInstance(game_info["Genre"], str)
        self.assertIn(game_info["Early Access"], ["Yes", "No"])
        # metacritic
        score = game_info["Metacritic"]
        metacritic_tests = [score == "No Score", type(score) == float]
        self.assertTrue(game_info["Metacritic"], any(metacritic_tests))
        self.assertIsInstance(game_info["Steam Review Percent"], float)
        self.assertIsInstance(game_info["Steam Review Total"], int)
        self.assertIsInstance(game_info["Release Year"], str)
        self.assertIsInstance(game_info["price"], str)
        self.assertIsInstance(game_info["discount"], float)
        self.assertIn(game_info["on_sale"], ["Yes", "No"])
        self.assertIsInstance(game_info["linux_compat"], str)
        self.assertIsInstance(game_info["drm_notice"], str)
        self.assertIsInstance(game_info["categories"], str)
        self.assertIsInstance(game_info["ext_user_account_notice"], str)

    def test_check_for_default(self):
        """
        Tests for default value when invalid game is given.
        """
        default_dict = {
            self.t.dev_col: "No Data",
            self.t.pub_col: "No Data",
            self.t.genre_col: "No Data",
            self.t.ea_col: "No",
            self.t.metacritic_col: "No Score",
            self.t.steam_rev_per_col: "No Reviews",
            self.t.steam_rev_total_col: "No Reviews",
            self.t.release_col: "No Year",
            "price": "No Data",
            "discount": 0.0,
            "on_sale": "No",
            "linux_compat": "Unsupported",
            "drm_notice": "No Data",
            "categories": "No Data",
            "ext_user_account_notice": "No Data",
        }
        self.assertEqual(self.t.get_game_info(None), default_dict)


class GetProfileUsername(unittest.TestCase):
    """
    Tests get_profile_username function.
    """

    def setUp(self):
        self.t = Tracker()

    def test_get_profile_username(self):
        gabe_username = "gabelogannewell"
        # ends with no /
        no_slash = "http://steamcommunity.com/id/gabelogannewell"
        result = self.t.get_profile_username(no_slash)
        self.assertEqual(result, gabe_username)
        # ends with /
        with_slash = "http://steamcommunity.com/id/gabelogannewell/"
        result = self.t.get_profile_username(with_slash)
        self.assertEqual(result, gabe_username)

    def test_False(self):
        string = "this is not a url"
        result = self.t.get_profile_username(string)
        self.assertFalse(result)


class GetSteamID(unittest.TestCase):
    """
    Tests get_steam_id function.
    """

    def setUp(self):
        self.t = Tracker()
        with open("configs\config.json") as file:
            data = json.load(file)
        self.t.steam_key = data["settings"]["steam_api_key"]

    def test_get_steam_id(self):
        # TODO move anything that uses an api or scraping to api test file
        gabe_steam_id = 76561197960287930
        result = self.t.get_steam_id("gabelogannewell")
        self.assertEqual(result, gabe_steam_id)

    def test_False(self):
        result = self.t.get_steam_id(".")
        self.assertFalse(result)


class ValidateSteamApiKey(unittest.TestCase):
    """
    Tests validate_steam_key function.
    Steam ID's must be allnumbers and 17 characters long.
    """

    def setUp(self):
        self.t = Tracker()

    def test_True(self):
        test_api_key = "15D4C014D419C0642B1E707BED41G7D4"
        result = self.t.validate_steam_key(test_api_key)
        self.assertTrue(result)

    def test_False(self):
        test_api_key = "15D4C014D419C0642B7D4"
        result = self.t.validate_steam_key(test_api_key)
        self.assertFalse(result)


class ValidateSteamID(unittest.TestCase):
    """
    Tests validate_steam_id function.
    Steam ID's must be allnumbers and 17 characters long.
    """

    def setUp(self):
        self.t = Tracker()

    def test_True(self):
        steam_ids = [
            76561197960287930,
            "76561197960287930",
        ]
        for id in steam_ids:
            with self.subTest(msg=type(id), id=id):
                result = self.t.validate_steam_id(id)
                self.assertTrue(result)

    def test_False(self):
        steam_ids = [
            765611028793,
            "asjkdhadsjdhjssaj",
        ]
        for id in steam_ids:
            with self.subTest(msg=type(id), id=id):
                result = self.t.validate_steam_id(id)
                self.assertFalse(result)


class IgnoreFunc(unittest.TestCase):
    """
    Tests get_game_info function.
    """

    def setUp(self):
        self.t = Tracker()

    def test_True(self):
        """
        Tests for True returns.
        """
        ignore_names = ["Half-Life 2: Lost Coast"]
        self.t.name_ignore_list = [string.lower() for string in ignore_names]
        self.t.appid_ignore_list = [61600, 12345864489]
        # appid return true
        self.assertTrue(self.t.should_ignore(appid=61600))
        self.assertTrue(self.t.should_ignore(appid=12345864489))
        # name return true
        self.assertTrue(self.t.should_ignore(name="Game Beta"))
        self.assertTrue(self.t.should_ignore(name="Squad - Public Testing"))
        self.assertTrue(self.t.should_ignore(name="Half-Life 2: Lost Coast"))

    def test_False(self):
        """
        Tests for False returns.
        """
        ignore_names = ["Half-Life 2: Lost Coast"]
        self.t.name_ignore_list = [string.lower() for string in ignore_names]
        # appid return false
        self.assertFalse(self.t.should_ignore(appid=345643))
        # name return false
        self.assertFalse(self.t.should_ignore(name="This is a great game"))

    def test_empty(self):
        """
        Empty args return False.
        """
        self.assertFalse(self.t.should_ignore())


class PlayStatus(unittest.TestCase):
    """
    Tests play_status function.
    """

    def setUp(self):
        self.t = Tracker()

    def test_base(self):
        """
        Tests average uses.
        """
        tests = [
            {"play_status": "Unplayed", "hours": 0.1, "ans": "Unplayed"},
            {"play_status": "Unplayed", "hours": 0.5, "ans": "Played"},
            {"play_status": "Unplayed", "hours": 1, "ans": "Playing"},
            {"play_status": "Unplayed", "hours": 0.5, "ans": "Played"},
            {"play_status": "Finished", "hours": 0.1, "ans": "Finished"},
        ]
        for a in tests:
            self.assertEqual(self.t.play_status(a["play_status"], a["hours"]), a["ans"])

    def test_do_nothing(self):
        """
        Tests Instances where nothing should be changed.
        """
        tests = [
            {"play_status": "Waiting", "hours": 100, "ans": "Waiting"},
            {"play_status": "Quit", "hours": 100, "ans": "Quit"},
            {"play_status": "Finished", "hours": 100, "ans": "Finished"},
            {"play_status": "Ignore", "hours": 100, "ans": "Ignore"},
        ]
        for a in tests:
            self.assertEqual(self.t.play_status(a["play_status"], a["hours"]), a["ans"])

    def test_play_status(self):
        tests = [
            # must play
            {"play_status": "Must Play", "hours": 0, "ans": "Must Play"},
            {"play_status": "Must Play", "hours": 0.5, "ans": "Played"},
            {"play_status": "Must Play", "hours": 1, "ans": "Playing"},
            # new game
            {"play_status": None, "hours": 0, "ans": "Unplayed"},
            {"play_status": None, "hours": 0.5, "ans": "Played"},
            {"play_status": None, "hours": 1, "ans": "Playing"},
            # error
            {"play_status": None, "hours": "Test", "ans": ""},
            {"play_status": "Unplayed", "hours": "Test", "ans": "Unplayed"},
        ]
        for test in tests:
            result = self.t.play_status(test["play_status"], test["hours"])
            self.assertEqual(result, test["ans"])

    def test_must_play(self):
        """
        Tests running on games previously set to "Must Play". This allows
        games to go back to normal status changing once they have been played.
        """
        tests = [
            {"play_status": "Must Play", "hours": 0, "ans": "Must Play"},
            {"play_status": "Must Play", "hours": 0.5, "ans": "Played"},
            {"play_status": "Must Play", "hours": 1, "ans": "Playing"},
        ]
        for a in tests:
            self.assertEqual(self.t.play_status(a["play_status"], a["hours"]), a["ans"])

    def test_must_play(self):
        """
        Tests running on new games.
        """
        tests = [
            {"play_status": None, "hours": 0, "ans": "Unplayed"},
            {"play_status": None, "hours": 0.5, "ans": "Played"},
            {"play_status": None, "hours": 1, "ans": "Playing"},
        ]
        for test in tests:
            result = self.t.play_status(test["play_status"], test["hours"])
            self.assertEqual(result, test["ans"])

    def test_error(self):
        """
        Tests for invalid values given causing nothing to be changed.
        """
        tests = [
            {"play_status": None, "hours": "Test", "ans": ""},
            {"play_status": "Unplayed", "hours": "Test", "ans": "Unplayed"},
        ]
        for test in tests:
            result = self.t.play_status(test["play_status"], test["hours"])
            self.assertEqual(result, test["ans"])


if __name__ == "__main__":
    unittest.main()