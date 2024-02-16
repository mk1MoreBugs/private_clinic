from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies import session_db
from app.routers import visits, doctors, patients, visiting_session
from app.schemas.base_item import BaseItem
from app.schemas.clinic_service import ClinicService
from app.schemas.patient_category import PatientCategory
from database.crud import diagnoses, doctor_categories
from database.crud import doctor_specialities
from database.crud import clinic_services
from database.crud import patients_categories


app = FastAPI()

app.include_router(visits.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(visiting_session.router)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/diagnoses")
async def get_diagnoses(
         session: Session = Depends(session_db),
) -> list[BaseItem]:
    list_diagnoses = diagnoses.read_diagnoses(session)

    return list_diagnoses


@app.get("/clinic-services")
async def get_clinic_services(
         session: Session = Depends(session_db),
) -> list[ClinicService]:
    list_clinic_services = clinic_services.read_clinic_services(session)

    return list_clinic_services


@app.get("/patient-categories")
async def get_patient_categories(
         session: Session = Depends(session_db),
) -> list[PatientCategory]:
    list_patient_categories = patients_categories.read_patient_categories(session)

    return list_patient_categories


@app.get("/doctor-categories")
async def get_doctor_categories(
         session: Session = Depends(session_db),
) -> list[BaseItem]:
    list_doctor_categories = doctor_categories.read_doctor_category(session)

    return list_doctor_categories


@app.get("/doctor-specialities")
async def get_doctor_specialities(
         session: Session = Depends(session_db),
) -> list[BaseItem]:
    list_doctor_categories = doctor_specialities.read_doctor_speciality(session)

    return list_doctor_categories
