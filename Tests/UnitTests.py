import unittest
import json
import sys
import os

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_dir)

from app import app

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_total_spending_by_user(self):
        response = self.app.get('/api/total_spent/17')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)


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


    def test_total_spending_above_1000(self):
        response = self.app.get('/api/total_spending_above_1000')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
