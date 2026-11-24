import unittest

import github


class RegressionTests(unittest.TestCase):
    def test_token_authentication(self):
        self.assertEqual(
            github.GitHub(access_token="fixture-token")._authorization, "token fixture-token"
        )

    def test_anonymous_authentication(self):
        self.assertIsNone(github.GitHub()._authorization)

    def test_response_mapping(self):
        self.assertEqual(github._parse_json('{"login":"octocat","id":1}').login, "octocat")

    def test_path_construction(self):
        self.assertEqual(
            str(github.GitHub().repos("owner")("repo")), "_Callable (/repos/owner/repo)"
        )
