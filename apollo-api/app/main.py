from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import calls, meet

app = FastAPI(title="Apollo API", version="0.1.0")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(calls.router)
app.include_router(meet.router)

@app.get("/")
async def root():
    return {"message": "Apollo API is running"}
