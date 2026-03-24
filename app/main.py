from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routers import links

app = FastAPI(title="URL Shortener Service")


app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/ui")
def ui():
    return FileResponse("app/static/index.html")

@app.get("/")
def root():
    return {"message": "URL Shortener API is running"}


app.include_router(links.router)


