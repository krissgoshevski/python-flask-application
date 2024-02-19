import unittest
from flask import Flask
from app import app  # Import your Flask app instance
import json

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):

        self.app = app.test_client()

    def test_get_total_spending_by_user(self):
        response = self.app.get('/api/total_spent/17')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on the expected response data

    def test_get_average_spending_by_age(self):
        response = self.app.get('/api/average_spending_by_age')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_total_spending_by_users(self):
        response = self.app.get('/api/total_spending_users')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_users_with_vouchers(self):
        response = self.app.get('/api/users/vouchers')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_total_spending_above_thousand(self):
        response = self.app.get('/api/total_spending_above_1000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
