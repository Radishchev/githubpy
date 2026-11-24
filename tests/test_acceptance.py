"""Actual HTTP calls to a local server enforcing GitHub's token-auth requirement."""

import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import github


class TokenOnlyApi(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.headers.get("Authorization") not in {"token fixture-token", "Bearer fixture-token"}:
            self.send_error(401, "Account passwords are unsupported; use a token")
            return
        if self.path != "/user":
            self.send_error(404)
            return
        body = b'{"login":"octocat","id":1}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class AuthenticationMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), TokenOnlyApi)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.original_url = github._URL
        github._URL = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        github._URL = cls.original_url
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def test_token_takes_precedence_over_legacy_password_arguments(self):
        client = github.GitHub(
            username="legacy-user", password="obsolete-password", access_token="fixture-token"
        )
        self.assertEqual(client.user.get().login, "octocat")

    def test_password_only_is_rejected_before_any_http_request(self):
        with self.assertRaisesRegex(ValueError, "access_token"):
            github.GitHub(username="legacy-user", password="obsolete-password")

    def test_partial_password_credentials_are_also_rejected(self):
        for credentials in ({"username": "legacy-user"}, {"password": "obsolete-password"}):
            with (
                self.subTest(credentials=credentials),
                self.assertRaisesRegex(ValueError, "access_token"),
            ):
                github.GitHub(**credentials)

    def test_existing_token_call_still_reaches_http_api(self):
        client = github.GitHub(access_token="fixture-token")
        self.assertEqual(client.user.get().id, 1)
