# Feature: Refresh Button and JSON View

## Context
Currently, the application requires users to re-enter credentials upon page refresh because it relies on a simple POST request rendering. Also, there is a need to inspect the raw JSON response for debugging or verification purposes.

## Goals
1.  Implement session persistence to allow page refreshes without re-login.
2.  Add a "Refresh Data" button that re-fetches the cost data using stored credentials.
3.  Add a collapsible section to the results page displaying the raw JSON response.

## Technical Plan

### 1. Session Management
*   **Library**: Use `starlette.middleware.sessions.SessionMiddleware` (built into FastAPI).
*   **Storage**: Store `client_id` and `client_secret` in the encrypted session cookie. Ideally, we would store an auth token, but since tokens expire and we want a simple "refresh" capability that might span longer than a token's life (or simplifies re-fetching logic), storing credentials allows us to always request a fresh token. *Note: In a production environment with stricter security, we might opt for a refresh token flow or server-side session storage, but for this tool, encrypted client-side session is acceptable.*
*   **Secret Key**: Needs a secret key for signing the session cookie. I'll generate a random one or read from env.

### 2. Routes Update (`main.py`)
*   `GET /`: Checks for session. If credentials exist, redirect to `/dashboard`. Else render login form.
*   `POST /login`:
    *   Validate credentials by fetching a token.
    *   If successful, store `client_id` and `client_secret` in `request.session`.
    *   Redirect to `/dashboard` (Post-Redirect-Get pattern).
*   `GET /dashboard`:
    *   Check `request.session` for `client_id` and `client_secret`.
    *   If missing, redirect to `/` (Login).
    *   If present, fetch token -> fetch cost data.
    *   Render `index.html` with data.
*   `GET /logout`:
    *   Clear `request.session`.
    *   Redirect to `/`.

### 3. Template Update (`templates/index.html`)
*   Add a "Refresh Data" button that links to `/dashboard`.
*   Add a `<details>` block.
*   Inside `<details>`, include a `<pre><code>` block containing the JSON data.
*   Use Jinja2 to dump the `costs` object to JSON string format.

### 4. Dependencies
*   Ensure `itsdangerous` is installed (standard with Starlette/FastAPI).

## Verification
*   Login flow works.
*   Refresing the `/dashboard` page works without asking for login.
*   "Refresh Data" button works.
*   Logout works.
*   JSON view is correct and collapsible.
