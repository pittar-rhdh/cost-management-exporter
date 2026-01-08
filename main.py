from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from services.cost_api import get_openshift_costs_by_cluster
from services.auth import get_access_token, AuthError
import os
import json

app = FastAPI(title="Red Hat Cost Management Exporter")

# Add Session Middleware
# Ideally the secret key should be in env vars, but we'll use a random one or fallback for this demo
SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "super-secret-key-for-demo-purposes")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Renders the login page.
    If session exists, redirect to dashboard.
    """
    if "client_id" in request.session and "client_secret" in request.session:
         return RedirectResponse(url="/dashboard")

    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request, 
    client_id: str = Form(...), 
    client_secret: str = Form(...)
):
    """
    Handles form submission:
    1. Authenticates with Client ID/Secret to verify they are valid.
    2. Stores credentials in session.
    3. Redirects to /dashboard.
    """
    try:
        # 1. Verify credentials by getting a token
        get_access_token(client_id, client_secret)
        
        # 2. Store in session
        request.session["client_id"] = client_id
        request.session["client_secret"] = client_secret
        
        # 3. Redirect
        return RedirectResponse(url="/dashboard", status_code=303)
        
    except AuthError as e:
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "error": f"Authentication Failed: {str(e)}"}
        )
    except Exception as e:
         return templates.TemplateResponse(
            "index.html", 
            {"request": request, "error": f"An unexpected error occurred: {str(e)}"}
        )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Fetches data using session credentials and renders the view.
    """
    client_id = request.session.get("client_id")
    client_secret = request.session.get("client_secret")

    if not client_id or not client_secret:
        return RedirectResponse(url="/")

    try:
        # 1. Get Token (fresh)
        token = get_access_token(client_id, client_secret)
        
        # 2. Fetch Data
        cost_data = get_openshift_costs_by_cluster(token)
        
        # 3. Render
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request, 
                "costs": cost_data,
                "json_output": json.dumps(cost_data, indent=2) 
            }
        )
    except AuthError as e:
        # If auth fails (e.g. credentials changed/revoked), clear session and redirect
        request.session.clear()
        return templates.TemplateResponse(
             "index.html", 
            {"request": request, "error": f"Session Expired or Invalid: {str(e)}"}
        )
    except Exception as e:
         return templates.TemplateResponse(
            "index.html", 
            {"request": request, "error": f"An unexpected error occurred: {str(e)}"}
        )

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
