import unittest
from unittest.mock import patch, MagicMock
from services.auth import get_access_token, AuthError
from services.cost_api import get_openshift_costs_by_cluster

class TestAuth(unittest.TestCase):
    @patch('services.auth.requests.post')
    def test_get_access_token_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "fake_access_token"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        token = get_access_token("client_id", "client_secret")
        self.assertEqual(token, "fake_access_token")

    def test_get_access_token_missing_creds(self):
        with self.assertRaises(AuthError):
            get_access_token("", "secret")
        with self.assertRaises(AuthError):
            get_access_token("id", "")

class TestCostApi(unittest.TestCase):
    @patch('services.cost_api.requests.get')
    def test_get_openshift_costs_success(self, mock_get):
        expected_data = {"data": []}
        mock_response = MagicMock()
        mock_response.json.return_value = expected_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        data = get_openshift_costs_by_cluster("fake_token")
        self.assertEqual(data, expected_data)

    @patch('services.cost_api.requests.get')
    def test_get_openshift_costs_failure(self, mock_get):
        mock_response = MagicMock()
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Network Error")

        data = get_openshift_costs_by_cluster("fake_token")
        self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()
