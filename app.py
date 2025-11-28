from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import blog, projects, static

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(blog.router)
app.include_router(projects.router)
app.include_router(static.router)
