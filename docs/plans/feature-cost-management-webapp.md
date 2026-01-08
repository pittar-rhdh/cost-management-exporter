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
-   [ ] Update `services/auth.py`:
    -   Change `get_access_token` to accept `client_id` and `client_secret`.
    -   Use the "Service Account" flow (Client Credentials Grant).
        -   Token URL: `https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token`
        -   Grant Type: `client_credentials`
-   [ ] Update `services/cost_api.py`:
    -   Function to query OpenShift costs needs to accept the `access_token` as an argument (since it's no longer global/env-based).

### 3. Web Application
-   [ ] Update `templates/index.html`:
    -   Add a Login Form (Client ID, Secret) if not authenticated.
    -   Display Cost Table if authenticated.
-   [ ] Update `main.py`:
    -   Add POST `/login` route to handle form submission.
    -   Validate credentials by attempting to get a token.
    -   If successful, render the cost view (passing the token/data).
    -   Ideally, use `FastAPI` sessions or just pass data in the context for this simple "stateless" approach (or re-fetch token on reload if we don't store it securely).
    -   *Decision*: For simplicity and security (avoiding complex session management for now), we will pass the credentials/token in the request loop or just re-authenticate. **Better approach**: Use a simple cookie or keep it in the rendered HTML as a hidden field (less secure) or just ask user to re-enter.
    -   *Refined Decision*: The user asked to "enter these values in the UI". We will have a form. When submitted, we fetch the data and display it. We won't implement a persistent login session for this V1 to keep it simple. Every refresh might require re-entry or we can use a basic browser cookie.
    -   Let's go with: **Form POST -> Fetch Data -> Render Page with Data**. If they refresh, they see the form again (unless we add browser-side persistence). This is simplest and meets "enter values in UI".

### 4. Testing & Verification
-   [ ] Update unit tests for `auth.py` to test Client Credentials flow.
-   [ ] Update integration tests.

## APIs Used
-   **Auth**: `https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token`
-   **Cost Management**: `https://console.redhat.com/api/cost-management/v1/reports/openshift/costs/`
