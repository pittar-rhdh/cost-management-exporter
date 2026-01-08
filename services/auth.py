import os
import requests
from dotenv import load_dotenv

load_dotenv()

class AuthError(Exception):
    pass

def get_access_token():
    """
    Exchanges the Offline Token for an Access Token.
    """
    offline_token = os.getenv("REDHAT_OFFLINE_TOKEN")
    if not offline_token:
        raise AuthError("REDHAT_OFFLINE_TOKEN not found in environment variables.")

    url = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": "cloud-services",
        "refresh_token": offline_token
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        raise AuthError(f"Failed to obtain access token: {e}")
