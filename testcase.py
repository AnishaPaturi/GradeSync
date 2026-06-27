import unittest
from unittest.mock import MagicMock, patch
from http.server import BaseHTTPRequestHandler, HTTPServer

class TestRequestHandler(unittest.TestCase):
    def setUp(self):
        self.request_handler = RequestHandler() # type: ignore
        self.request_handler.connection = MagicMock()
        self.request_handler.cursor = MagicMock()

    @patch('urllib.parse.parse_qs')
    @patch('urllib.parse.urlparse')
    def test_do_GET_display_students(self, mock_urlparse, mock_parse_qs):
        # Set up the mock objects
        mock_urlparse.return_value.path = "/display_students"
        mock_parse_qs.return_value = {"id": ["1"]}

        # Call the method being tested
        self.request_handler.do_GET()

        # Assert that the correct SQL query was executed
        self.request_handler.cursor.execute.assert_called_with("SELECT * FROM students WHERE id=%s", (1,))

    @patch('urllib.parse.parse_qs')
    @patch('urllib.parse.urlparse')
    def test_do_GET_class_average(self, mock_urlparse, mock_parse_qs):
        # Set up the mock objects
        mock_urlparse.return_value.path = "/class_average"

        # Call the method being tested
        self.request_handler.do_GET()

        # Assert that the correct SQL query was executed
        self.request_handler.cursor.execute.assert_called_with("SELECT AVG(grade) FROM students")

    @patch('urllib.parse.parse_qs')
    @patch('urllib.parse.urlparse')
    def test_do_GET_not_found(self, mock_urlparse, mock_parse_qs):
        # Set up the mock objects
        mock_urlparse.return_value.path = "/non_existent_path"

        # Call the method being tested
        self.request_handler.do_GET()

        # Assert that a 404 response was sent
        self.request_handler.send_response.assert_called_with(404)

if __name__ == '__main__':
    unittest.main()