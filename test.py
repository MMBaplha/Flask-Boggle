import unittest
from app import app
from flask import session
from unittest.mock import patch

class BoggleAppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and activate app context."""

        self.client = app.test_client()
        self.client.testing = True

    def test_home(self):
        """Test that the home route sets up board, highscore, and nplays in session."""

        with self.client as client:
            response = client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<title>Boggle</title>', response.data)
            self.assertIn('board', session)
            self.assertIn('highscore', session)
            self.assertIn('nplays', session)

    @patch('app.boggle_game.check_valid_word')
    def test_submit_guess(self, mock_check_valid_word):
        """Test submit_guess route with various inputs."""

        mock_check_valid_word.return_value = "ok"  # Simulate valid word

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [['C', 'A', 'T', 'D', 'O'], 
                                 ['S', 'O', 'A', 'R', 'E'], 
                                 ['R', 'E', 'A', 'D', 'S'], 
                                 ['F', 'I', 'L', 'E', 'S'], 
                                 ['B', 'O', 'O', 'K', 'S']]

            response = client.post("/submit_guess", json={"guess": "CAT"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], "ok")

            response = client.post("/submit_guess", json={"guess": ""})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json['result'], "no-guess")

    def test_end_game(self):
        """Test end_game route updates high score and nplays."""
        
        with self.client as client:
            with client.session_transaction() as sess:
                sess['nplays'] = 2
                sess['highscore'] = 10

            response = client.post("/end_game", json={"score": 15})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['new_highscore'], 15)
            self.assertEqual(response.json['nplays'], 3)

            response = client.post("/end_game", json={"score": 5})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['new_highscore'], 15)  # High score should remain 15
            self.assertEqual(response.json['nplays'], 4)

if __name__ == "__main__":
    unittest.main()