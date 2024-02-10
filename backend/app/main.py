from fastapi import FastAPI

from app.routers import visits, doctors, patients, visiting_session

app = FastAPI()


app.include_router(visits.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(visiting_session.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
