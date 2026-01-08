import requests
from .auth import get_access_token

API_BASE_URL = "https://console.redhat.com/api/cost-management/v1/reports/openshift/costs/"

def get_openshift_costs_by_cluster():
    """
    Queries the Red Hat Cost Management API for OpenShift costs,
    aggregated by cluster for the current month.
    """
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    params = {
        "filter[time_scope_units]": "month",
        "filter[time_scope_value]": "-1",
        "filter[resolution]": "monthly",
        "group_by[cluster]": "*"
    }

    try:
        response = requests.get(API_BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cost data: {e}")
        return None
