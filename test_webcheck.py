
import unittest
from unittest.mock import patch
import urllib.error

from webcheck import normalize_url, check_website


class TestNormalizeURL(unittest.TestCase):

    def test_adds_https(self):
        self.assertEqual(
            normalize_url("google.com"),
            "https://google.com"
        )

    def test_preserves_http(self):
        self.assertEqual(
            normalize_url("http://example.com"),
            "http://example.com"
        )

    def test_rejects_empty_url(self):
        with self.assertRaises(ValueError):
            normalize_url("")


class TestCheckWebsite(unittest.TestCase):

    @patch("webcheck.urllib.request.urlopen")
    def test_successful_response(self, mock_urlopen):
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.status = 200

        result = check_website("https://example.com")

        self.assertEqual(result["status_code"], 200)
        self.assertTrue(result["reachable"])
        self.assertTrue(result["available"])
        self.assertEqual(result["error"], "")

    @patch("webcheck.urllib.request.urlopen")
    def test_http_404_response(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.HTTPError(
            "https://example.com/missing",
            404,
            "Not Found",
            {},
            None
        )

        result = check_website("https://example.com/missing")

        self.assertEqual(result["status_code"], 404)
        self.assertTrue(result["reachable"])
        self.assertFalse(result["available"])
        self.assertEqual(result["error"], "HTTP error: 404")

    @patch("webcheck.urllib.request.urlopen")
    def test_connection_failure(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("Connection failed")

        result = check_website("https://example.com")

        self.assertIsNone(result["status_code"])
        self.assertFalse(result["reachable"])
        self.assertFalse(result["available"])
        self.assertIn("Connection failed", result["error"])


if __name__ == "__main__":
    unittest.main()
