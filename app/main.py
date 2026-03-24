from fastapi import FastAPI
from app.routers import links

app = FastAPI(title="URL Shortener Service")


app.include_router(links.router)

@app.get("/")
def root():
    return {"message": "URL Shortener API is running"}