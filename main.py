from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.cost_api import get_openshift_costs_by_cluster
from services.auth import get_access_token, AuthError

app = FastAPI(title="Red Hat Cost Management Exporter")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Renders the login page (or data if we had session persistence, which we are skipping for V1).
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login_and_fetch(
    request: Request, 
    client_id: str = Form(...), 
    client_secret: str = Form(...)
):
    """
    Handles form submission:
    1. Authenticates with Client ID/Secret.
    2. Fetches Cost Data using the token.
    3. Renders the page with the data.
    """
    try:
        # 1. Get Token
        token = get_access_token(client_id, client_secret)
        
        # 2. Fetch Data
        cost_data = get_openshift_costs_by_cluster(token)
        
        # 3. Render
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "costs": cost_data}
        )
        
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
