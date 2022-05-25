from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        
        """Setting up tests"""
        
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        
        """Ensure that there is something in the session and HTML is displayed on the screen"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIn(b'High Score:', response.data)
            self.assertIn(b'Score:', response.data)

    def test_valid_word(self):
        
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["D", "A", "R", "T", "S"], 
                                 ["O", "L", "P", "C", "X"], 
                                 ["P", "E", "C", "D", "V"], 
                                 ["A", "T", "N", "S", "P"], 
                                 ["D", "R", "I", "W", "R"]]
        response = self.client.get('/check-word?word=dart')
        response = self.client.get('/check-word?word=sin')
        response = self.client.get('/check-word?word=pet')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        
        """Checking for word that is NOT on the board"""
        self.client.get('/')
        response = self.client.get('/check-word?word=refrigerator')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        
        """Checking to see if the word being tested is an English word"""
        self.client.get('/')
        response = self.client.get(
            '/check-word?word=kafjfjalfjasfafkjas')
        self.assertEqual(response.json['result'], 'not-word')