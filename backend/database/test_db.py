from datetime import date

import pytest

from database.crud import create_patient_categories, read_patient_categories, create_patient, read_patient
from database.database import create_db
from database.models.base import Base
from database.models.patient import Patient
from database.models.patient_category import PatientCategory





@pytest.fixture(scope="module")
def db_session():
    yield create_db("sqlite://", echo=True)

@pytest.fixture(scope="module")
def patient_category():
    return PatientCategory(
        category="test category",
        discount_percentage=10,
    )

@pytest.fixture(scope="module")
def patients(patient_category):
    return [
        Patient(
            last_name="Иванов1",
            first_name="Иван1",
            middle_name="Иванович1",
            birthday=date.fromisoformat("1999-12-04"),
        ),
        Patient(
            last_name="Иванов2",
            first_name="Иван2",
            middle_name="Иванович2",
            birthday=date.fromisoformat("1995-12-10"),
            category_id=0,

        ),
    ]


def test_create_table(db_session):
    assert len(Base.metadata.tables.keys()) == 9


def test_create_patient_categories(db_session, patient_category):
    create_patient_categories(
        session=db_session,
        category=patient_category.category,
        discount_percentage=patient_category.discount_percentage,
    )
    result = read_patient_categories(session=db_session)

    assert result[0].category == patient_category.category
    assert result[0].discount_percentage == patient_category.discount_percentage


def test_create_patient(db_session, patients, patient_category):
    create_patient(
        session=db_session,
        last_name=patients[0].last_name,
        first_name=patients[0].first_name,
        middle_name=patients[0].middle_name,
        birthday=patients[0].birthday,
    )

    create_patient(
        session=db_session,
        last_name=patients[1].last_name,
        first_name=patients[1].first_name,
        middle_name=patients[1].middle_name,
        birthday=patients[1].birthday,
        category_id=patients[1].category_id,
    )

    result = read_patient(session=db_session)
    print("\n", result)

    assert result[0].last_name == patients[0].last_name
    assert result[0].first_name == patients[0].first_name
    assert result[0].middle_name == patients[0].middle_name
    assert result[0].birthday == patients[0].birthday
    assert result[0].category_id is None

    assert result[1].last_name == patients[1].last_name
    assert result[1].first_name == patients[1].first_name
    assert result[1].middle_name == patients[1].middle_name
    assert result[1].birthday == patients[1].birthday
    assert result[1].category_id == patients[1].category_id

