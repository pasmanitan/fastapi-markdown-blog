from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

html_dir = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", "static", "html")
)

html_pages = Jinja2Templates(directory=f"{html_dir}")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return html_pages.TemplateResponse(request=request, name="home.html")


@router.get("/about-me", response_class=HTMLResponse)
async def about_me(request: Request):
    return html_pages.TemplateResponse(request=request, name="about-me.html")
