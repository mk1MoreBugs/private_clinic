from fastapi import FastAPI

from app.routers import visits


app = FastAPI()

app.include_router(visits.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
