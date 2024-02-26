import unittest
import sys
import os
from app import app
from unittest.mock import MagicMock
import json

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(project_dir)

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.mocked_query = MagicMock()

    def test_get_total_spending_by_user(self):
        user_id = 17
        response = self.app.get(f'/api/total_spent/{user_id}')
        data = json.loads(response.data)

        if response.status_code == 200:
            self.assertEqual(response.status_code, 200)
        elif response.status_code == 404:
            self.assertEqual(response.status_code, 404)
            self.fail(
                f"User was now found, received status code {response.status_code}")
        else:
            self.assertEqual(response.status_code, 406)
            self.fail(
                f"The user with ID {user_id} has not spent money yet. Received status code {response.status_code}")

    def test_get_average_spending_by_age(self):
        response = self.app.get('/api/average_spending_by_age')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['18-24'], 150.0)
        self.assertEqual(data['25-30'], 262.5)
        self.assertEqual(data['31-36'], 0.0)
        self.assertEqual(data['37-47'], 3367103.3)
        self.assertEqual(data['48-99'], 3563.3)



    def test_get_total_spending_by_users(self):
        response = self.app.get('/api/total_spending_users')
        data = json.loads(response.data)

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Assert response data
        expected_data = {"total_spending_users": 10113350.0}
        self.assertEqual(data, expected_data)

    def test_get_users_with_vouchers(self):
        response = self.app.get('/api/users/vouchers')
        data = json.loads(response.data)

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Assert response data
        expected_data = {
            "users_for_voucher": [
                {
                    "age": 47,
                    "email": "amy59@example.com",
                    "name": "Katherine Porter",
                    "user_id": 3
                },
                {
                    "age": 95,
                    "email": "mitchelljeremy@example.net",
                    "name": "random user",
                    "user_id": 17
                }
            ]
        }
        self.assertEqual(data, expected_data)

    def test_total_spending_above_1000(self):
        response = self.app.get('/api/total_spending_above_1000')
        data = json.loads(response.data)

        # Assert response status code
        self.assertEqual(response.status_code, 200)

        # Assert response data
        expected_data = [
            {
                "total_spending": 10090.0,
                "user_id": 17
            },
            {
                "total_spending": 10101000.0,
                "user_id": 3
            }
        ]
        self.assertEqual(data, expected_data)


if __name__ == '__main__':
    unittest.main()
