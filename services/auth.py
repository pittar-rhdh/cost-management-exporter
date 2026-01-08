import requests

class AuthError(Exception):
    pass

def get_access_token(client_id, client_secret):
    """
    Exchanges Client ID and Secret for an Access Token using Client Credentials Grant.
    """
    if not client_id or not client_secret:
        raise AuthError("Client ID and Client Secret are required.")

    url = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        raise AuthError(f"Failed to obtain access token: {e}")
