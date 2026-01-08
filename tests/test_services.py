import unittest
from unittest.mock import patch, MagicMock
from services.auth import get_access_token, AuthError
from services.cost_api import get_openshift_costs_by_cluster
import os

class TestAuth(unittest.TestCase):
    @patch('services.auth.requests.post')
    @patch('services.auth.os.getenv')
    def test_get_access_token_success(self, mock_getenv, mock_post):
        mock_getenv.return_value = "fake_offline_token"
        
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "fake_access_token"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        token = get_access_token()
        self.assertEqual(token, "fake_access_token")

    @patch('services.auth.os.getenv')
    def test_get_access_token_missing_env(self, mock_getenv):
        mock_getenv.return_value = None
        with self.assertRaises(AuthError):
            get_access_token()

class TestCostApi(unittest.TestCase):
    @patch('services.cost_api.get_access_token')
    @patch('services.cost_api.requests.get')
    def test_get_openshift_costs_success(self, mock_get, mock_get_token):
        mock_get_token.return_value = "fake_token"
        
        expected_data = {"data": []}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        data = get_openshift_costs_by_cluster()
        self.assertEqual(data, expected_data)

    @patch('services.cost_api.get_access_token')
    @patch('services.cost_api.requests.get')
    def test_get_openshift_costs_failure(self, mock_get, mock_get_token):
        mock_get_token.return_value = "fake_token"
        
        mock_response = MagicMock()
        # Simulate an exception raising from raise_for_status
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response
        # Depending on implementation, requests.exceptions.RequestException is usually caught
        # Let's adjust mock to raise RequestException
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Network Error")

        data = get_openshift_costs_by_cluster()
        self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()
