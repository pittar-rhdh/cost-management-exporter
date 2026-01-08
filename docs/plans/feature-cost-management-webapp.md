# Plan: Red Hat Cost Management Web App

## Objective
Build a Python Web Application using FastAPI to query the Red Hat Cost Management API and display OpenShift cost information aggregated by Cluster for the current month.

## Architecture

### Components
1.  **Web Server**: FastAPI (modern, fast, easy to use).
2.  **API Client**: `requests` library to handle communication with `api.access.redhat.com` (Auth) and `console.redhat.com` (Cost API).
3.  **Configuration**: `python-dotenv` to manage sensitive credentials (Offline Token).
4.  **Frontend**: Server-side rendered HTML using `Jinja2` templates.

### Data Flow
1.  User visits the homepage (`/`).
2.  Server checks for a valid Access Token.
    -   If missing or expired, exchanges the Offline Token (from `.env`) for a new Access Token.
3.  Server calls the Red Hat Cost Management API:
    -   Endpoint: `/api/cost-management/v1/reports/openshift/costs/`
    -   Parameters:
        -   `filter[time_scope_units]=month`
        -   `filter[time_scope_value]=-1` (Current month)
        -   `group_by[cluster]=*`
4.  Server renders `index.html` with the retrieved cost data.

## Implementation Steps

### 1. Project Setup
-   [ ] Create git branch `feature/cost-management-webapp`.
-   [ ] Create `docs/plans/feature-cost-management-webapp.md` (This file).
-   [ ] Update `requirements.txt`:
    -   `fastapi`
    -   `uvicorn`
    -   `requests`
    -   `python-dotenv`
    -   `jinja2`
    -   `httpx` (optional, but good for async, sticking to requests for simplicity unless needed).
-   [ ] Create `.env.example` template.

### 2. Core Logic (API Client)
-   [ ] Create `services/` directory.
-   [ ] Implement `services/auth.py` (or similar):
    -   Function to exchange Offline Token for Access Token.
-   [ ] Implement `services/cost_api.py`:
    -   Function to query OpenShift costs with specific grouping and date filtering.

### 3. Web Application
-   [ ] Rename/Update `app.py` or create `main.py` as the entry point.
-   [ ] Configure FastAPI with static files (if needed) and templates.
-   [ ] Create `templates/index.html`:
    -   Simple Bootstrap table to display Cluster Name and Cost.
-   [ ] Implement GET `/` route to orchestrate the data fetching and rendering.

### 4. Testing & Verification
-   [ ] Write unit tests for the API client (mocking external calls).
-   [ ] Write integration test for the FastAPI route.
-   [ ] Run the application and manually verify with live credentials (if available) or mocks.

## APIs Used
-   **Auth**: `https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token`
-   **Cost Management**: `https://console.redhat.com/api/cost-management/v1/reports/openshift/costs/`
