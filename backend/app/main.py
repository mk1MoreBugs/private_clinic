from datetime import date

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.dependencies import session_db
from app.routers import visits, doctors, patients
from database.crud.patients import create_patient, read_patients

app = FastAPI()


app.include_router(visits.router)
app.include_router(doctors.router)
app.include_router(patients.router)


@app.get("/")
async def root(session: Session = Depends(session_db)):
    create_patient(
        session=session,
        last_name="bar",
        first_name="baz",
        middle_name="barbar",
        birthday=date.fromisoformat("1999-12-04"),
    )

    patients_1 = read_patients(session)

    return {"message": "Hello World", "patients_1": patients_1}
