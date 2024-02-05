from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#  For Base.metadata.create_all(engine)
from .models.diagnosis import Diagnosis
from .models.doctor import Doctor
from .models.doctor_category import Category
from .models.doctor_speciality import Speciality
from .models.patient import Patient
from .models.patient_category import PatientCategory
from .models.service import Service
from .models.visit import Visit
from .models.visiting_session import VisitingSession

from database.models.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"


def create_db(database_url=SQLALCHEMY_DATABASE_URL, echo=False):
    engine = create_engine(database_url, echo=echo)
    Base.metadata.create_all(engine)
    return sessionmaker(engine)
