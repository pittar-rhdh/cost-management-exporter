from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.cost_api import get_openshift_costs_by_cluster
from services.auth import AuthError

app = FastAPI(title="Red Hat Cost Management Exporter")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        cost_data = get_openshift_costs_by_cluster()
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "costs": cost_data}
        )
    except AuthError as e:
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "error": f"Authentication Error: {str(e)}"}
        )
    except Exception as e:
         return templates.TemplateResponse(
            "index.html", 
            {"request": request, "error": f"An unexpected error occurred: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
