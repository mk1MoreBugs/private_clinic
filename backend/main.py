from fastapi import FastAPI

from app.routers import visits, doctors, patients

app = FastAPI()

app.include_router(visits.router)
app.include_router(doctors.router)
app.include_router(patients.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
