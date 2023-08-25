"""
# -*- coding: utf-8 -*-

Created on Aug 2023
@author: Prateek Yadav

"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../src')

import json
import unittest
from server import flaskApplication

class TestPredictionAPI(unittest.TestCase):

    def setUp(self):
        self.app = flaskApplication.test_client()

    def test_hello(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello!', response.data)

    def test_predict_valid_input(self):
        input_data = {'input': 'This is a valid sentence.'}
        response = self.app.post('/pred', data=json.dumps(input_data), content_type='application/json')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('predictions', data)
        self.assertTrue(isinstance(data['predictions'], str))

    def test_predict_invalid_short_input(self):
        input_data = {'input': 'short.'}
        response = self.app.post('/pred', data=json.dumps(input_data), content_type='application/json')
        data = response.get_json()

        self.assertEqual(response.status_code, 420)
        self.assertIn('error', data)
        self.assertIn('Invalid input', data['error'])

    def test_predict_invalid_max_len_input(self):
        input_data = {'input': ' '.join(['hi']*150)}
        response = self.app.post('/pred', data=json.dumps(input_data), content_type='application/json')
        data = response.get_json()

        self.assertEqual(response.status_code, 420)
        self.assertIn('error', data)
        self.assertIn('Invalid input', data['error'])

    def test_predict_missing_input(self):
        input_data = {}
        response = self.app.post('/pred', data=json.dumps(input_data), content_type='application/json')
        data = response.get_json()

        self.assertEqual(response.status_code, 420)
        self.assertIn('error', data)
        self.assertIn('"input" argument missing', data['error'])


if __name__ == '__main__':
    unittest.main()
