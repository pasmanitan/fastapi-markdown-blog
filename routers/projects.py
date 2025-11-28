from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

html_dir = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", "static", "html")
)

html_pages = Jinja2Templates(directory=f"{html_dir}")

projects_dir = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../",
        "static",
        "markdown",
        "projects",
    )
)

markdown_path = Jinja2Templates(directory=f"{projects_dir}")


@router.get("/projects", response_class=HTMLResponse)
async def projects(request: Request):
    return html_pages.TemplateResponse(request=request, name="projects.html")
