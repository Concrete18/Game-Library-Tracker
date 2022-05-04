import unittest
import datetime as dt

# classes
from Game_Tracker import Tracker


class TestStringMethods(unittest.TestCase):
    def test_get_year(self):
        print("\n", "get_year")
        tester = Tracker()
        date_tests = {
            "this is not a date": "Invalid Date",
            "Sep 14, 2016": "2016",
            "25 Apr, 1991": "1991",
            "16 Nov, 2009": "2009",
            "Mai 25, 1991": "1991",
            "Apr , 2015": "2015",
        }
        for date, bool in date_tests.items():
            self.assertEqual(tester.get_year(date), bool)

    def test_get_app_id(self):
        print("\n", "get_app_id")
        tester = Tracker()
        app_id_tests = {
            "Inscryption": 1092790,
            "Dishonored 2": 403640,
            "Deep Rock Galactic": 548430,
        }
        for name, answer in app_id_tests.items():
            self.assertEqual(tester.get_app_id(name), answer)

    def test_get_game_info(self):
        print("\n", "get_game_info")
        tester = Tracker()
        # checks using the app id for Deep Rock Galactic
        dict = tester.get_game_info(1145360)
        keys = ["name", "developers", "publishers"]
        for key in keys:
            self.assertIn(key, dict.keys())

    def test_get_metacritic(self):
        print("\n", "get_metacritic")
        tester = Tracker()
        metacritic_tests = {
            "Dishonored 2": 86,
            "Deep Rock Galactic": 85,
            "Inscryption": 85,
            "Not a Real Game": "Page Error",
        }
        for name, answer in metacritic_tests.items():
            self.assertEqual(tester.get_metacritic(name, "pc"), answer)

    def test_steam_deck_compat(self):
        print("\n", "steam_deck_compat")
        tester = Tracker()
        steam_deck_tests = {
            1167630: "PLAYABLE",
            667970: "UNSUPPORTED",
            1579380: "UNKNOWN",
            1145360: "VERIFIED",
            204080: "VERIFIED",
            # Deathloop check has empty results from the api
            # 1457700: "VERIFIED",
            204080: False,
        }
        for app_id, status in steam_deck_tests.items():
            self.assertEqual(tester.steam_deck_compat(app_id), status)

    def test_hours_played(self):
        print("\n", "hours_played")
        tester = Tracker()
        time_hours_played = {
            800: 13.3,
            30: 0.5,
            2940: 49,
        }
        for minutes_played, answer in time_hours_played.items():
            self.assertEqual(tester.hours_played(minutes_played), answer)

    def test_time_passed(self):
        print("\n", "convert_time_passed")
        tester = Tracker()
        time_passed_tests = {
            800: "13.3 Hour(s)",
            30: "30 Minute(s)",
            2940: "2.0 Day(s)",
        }
        for minutes_played, answer in time_passed_tests.items():
            self.assertEqual(tester.convert_time_passed(minutes_played), answer)

    def test_days_since(self):
        print("\n", "days_since")
        tester = Tracker()
        date_tests = {
            2: dt.datetime(2022, 4, 22),
            10: dt.datetime(2022, 4, 14),
            365: dt.datetime(2021, 4, 24),
        }
        past_date = dt.datetime(2022, 4, 24)
        for answer, current_date in date_tests.items():
            self.assertEqual(tester.days_since(current_date, past_date), answer)

    def test_get_store_link(self):
        print("\n", "get_store_link")
        tester = Tracker()
        store_link_tests = {
            "752590": "https://store.steampowered.com/app/752590/",
            "629730": "https://store.steampowered.com/app/629730/",
        }
        for app_id, answer in store_link_tests.items():
            self.assertEqual(tester.get_store_link(app_id), answer)
            # tests that the url exists
            response = tester.request_url(answer)
            self.assertIn(app_id, response.url)
            self.assertTrue(response)
        # test for broken link that redirects due to app id not being found
        invalid_url = "https://store.steampowered.com/app/6546546545465484213211545730/"
        response = tester.request_url(invalid_url)
        self.assertNotIn("6546546545465484213211545730", response.url)

    def test_url_sanitize(self):
        print("\n", "url_sanitize")
        tester = Tracker()
        url_tests = {
            "Hood: Outlaws & Legends": "hood-outlaws-legends",
            "This is a (test), or is it?": "this-is-a-test-or-is-it",
            "Blade & Sorcery": "blade-sorcery",
        }
        for string, result in url_tests.items():
            self.assertEqual(tester.url_sanitize(string), result)

    def test_play_status(self):
        print("\n", "play_status")
        tester = Tracker()
        tests = [
            {"play_status": "Unplayed", "hours": 0.1, "ans": "Unplayed"},
            {"play_status": "Unplayed", "hours": 0.5, "ans": "Played"},
            {"play_status": "Unplayed", "hours": 1, "ans": "Playing"},
            {"play_status": "Unplayed", "hours": 0.5, "ans": "Played"},
            {"play_status": "Finished", "hours": 0.1, "ans": "Finished"},
            # do nothing
            {"play_status": "Waiting", "hours": 100, "ans": "Waiting"},
            {"play_status": "Quit", "hours": 100, "ans": "Quit"},
            {"play_status": "Finished", "hours": 100, "ans": "Finished"},
            {"play_status": "Ignore", "hours": 100, "ans": "Ignore"},
            # new game
            {"play_status": "", "hours": 0, "ans": "Unplayed"},
            {"play_status": "", "hours": 0.5, "ans": "Played"},
            {"play_status": "", "hours": 1, "ans": "Playing"},
            # error
            {"play_status": "", "hours": "Test", "ans": ""},
            {"play_status": "Unplayed", "hours": "Test", "ans": "Unplayed"},
        ]
        for a in tests:
            self.assertEqual(tester.play_status(a["play_status"], a["hours"]), a["ans"])

    def test_lev_distance(self):
        print("\n", "lev_distance")
        tester = Tracker()
        string_tests = [
            # insert
            {"word1": "test", "word2": "tests", "ans": 1},
            # delete
            {"word1": "bolt", "word2": "bot", "ans": 1},
            # replace
            {"word1": "spell", "word2": "spelt", "ans": 1},
            # insert, delete and replace
            {"word1": "Thinking", "word2": "Thoughts", "ans": 6},
        ]
        for a in string_tests:
            self.assertEqual(tester.lev_distance(a["word1"], a["word2"]), a["ans"])

    def test_string_matcher(self):
        print("\n", "string_matcher")
        tester = Tracker()
        test_list = [
            "This is a test, yay",
            "this is not it, arg",
            "Find the batman!",
            "Shadow Tactics: Blades of the Shogun - Aiko's Choice",
            "The Last of Us",
            "Elden Ring",
            "The Last of Us Part I",
            "The Last of Us Part II",
            "Waltz of the Wizard: Natural Magic",
            "Life is Strange™",
            "The Witcher 3: Wild Hunt",
            "Marvel's Spider-Man: Miles Morales",
            "Crypt Of The Necrodancer: Nintendo Switch Edition",
        ]
        string_tests = {
            "This is a test": "This is a test, yay",
            "find th bamtan": "Find the batman!",
            "Eldn Rings": "Elden Ring",
            "Shadow Tactics Blades of the Shougn Aikos Choce": "Shadow Tactics: Blades of the Shogun - Aiko's Choice",
            "the last of us": "The Last of Us",
            "Walk of the Wizard: Natural Magik": "Waltz of the Wizard: Natural Magic",
            "The last of us Part I": "The Last of Us Part I",
            "Life is Strange 1": "Life is Strange™",
            "Witcher 3: The Wild Hunt": "The Witcher 3: Wild Hunt",
            "Spider-Man: Miles Morales": "Marvel's Spider-Man: Miles Morales",
            "grave Of The deaddancer: Switch Edition": "Crypt Of The Necrodancer: Nintendo Switch Edition",
        }
        for string, answer in string_tests.items():
            self.assertEqual(
                tester.string_matcher2(string, test_list, debug=True)[0],
                answer,
            )
            # self.assertEqual(
            #     tester.string_matcher(string, test_list, debug=True), answer
            # )


if __name__ == "__main__":
    unittest.main()
