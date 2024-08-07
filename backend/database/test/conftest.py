from datetime import date, datetime
from sqlalchemy.orm import Session

import pytest

from .. import PatientCategory
from ..database import create_db_tables_and_engine


@pytest.fixture()
def db_session():
    engine = create_db_tables_and_engine("sqlite://", echo=True)
    with Session(engine) as session:
        return session


@pytest.fixture()
def doctor_categories():
    return {
        "second": "Вторая категория",
        "first": "Первая категория",
        "highest": "Высшая категория",
    }


@pytest.fixture()
def doctor_specialities():
    return ["foo", "bar", "baz"]


@pytest.fixture()
def doctors():
    return [
        {
            "user_id": 1,
            "experience": 10,
            "speciality_id": 1,
            "category_id": 1,
        },
        {
            "user_id": 2,
            "experience": 5,
            "speciality_id": 2,
            "category_id": 2,
        },
        {
            "user_id": 3,
            "experience": 15,
            "speciality_id": 3,
            "category_id": 3,
        },
        {
            "user_id": 4,
            "experience": 1,
            "speciality_id": 3,
            "category_id": 3,
        },
    ]


@pytest.fixture()
def patients():
    return [
        {
            "user_id":  5,
            "birthday": date.fromisoformat("1999-12-04"),
            "category_name": None,
            "category_id": None,
        },
        {
            "user_id":  6,
            "birthday": date.fromisoformat("1995-12-10"),
            "category_name": "bar",
            "category_id": 1,
        },
        {
            "user_id":  7,
            "birthday": date.fromisoformat("1995-12-10"),
            "category_name": "bar",
            "category_id": 1,
        },
    ]


@pytest.fixture()
def patient_categories():
    return [
        PatientCategory(
            name="test category",
            discount_percentage=10,
        ),
        PatientCategory(
            name="test category 2",
            discount_percentage=25,
        ),
    ]


@pytest.fixture()
def users():
    return [
        {
            "id": 1,
            "last_name": "Фамилия",
            "first_name": "ИмяДоктор",
            "middle_name": "Отчство",
            "hashed_password": "",
        },
        {
            "id": 2,
            "last_name": "Фамилия2",
            "first_name": "Имя",
            "middle_name": "Отчство",
            "hashed_password": "",
        },
        {
            "id": 3,
            "last_name": "Фамилия3",
            "first_name": "Имя",
            "middle_name": "Отчство",
            "hashed_password": "",
        },
        {
            "id": 4,
            "last_name": "Фамилия4",
            "first_name": "Имя",
            "middle_name": "Отчство",
            "hashed_password": "",
        },
        {
            "id": 5,
            "last_name": "Фамилия5",
            "first_name": "Имя",
            "middle_name": "Отчство",
            "hashed_password": "",
        },
        {
            "id": 6,
            "last_name": "Фамилия6",
            "first_name": "Имя",
            "middle_name": None,
            "hashed_password": "",
        },
        {
            "id": 7,
            "last_name": "Фамилия7",
            "first_name": "ИмяПациент",
            "middle_name": None,
            "hashed_password": "",
        },
    ]


@pytest.fixture()
def services_clinic():
    return [
        {
            "name": "foo",
            "price": 100,
        },
        {
            "name": "bar",
            "price": 500,
        },
        {
            "name": "baz",
            "price": 800,
        },
    ]


@pytest.fixture()
def diagnosis():
    return [
        {"name": "foo"},
        {"name": "bar"},
        {"name": "baz"},
    ]


@pytest.fixture()
def visiting_sessions():
    return [
        {
            'patient_id': 5,
            'visiting_session_id': 1,
         },
        {
            'patient_id': 6,
            'visiting_session_id': 2,
        },
        {
            "patient_id": 7,
            'visiting_session_id': 3,
        },
    ]


@pytest.fixture()
def visits():
    return [
        {
            'patient_id': 7,
            'visiting_session_id': 3,
            'service_id': 1,
            'doctor_id': 3,
            'appointment_date': datetime.fromisoformat("2023-03-15"),
            'discounted_price': 800,
            'diagnosis_id': None,
            'anamnesis': None,
            'opinion': None,
        },
        {
            'patient_id': 7,
            'visiting_session_id': 3,
            'service_id': 1,
            'doctor_id': 1,
            'appointment_date': datetime.fromisoformat("2023-03-20"),
            'discounted_price': 250,
            'diagnosis_id': 1,
            'anamnesis': "foo bar baz",
            'opinion': "baz, bar, foo",
        },
        {
            'patient_id': 5,
            'visiting_session_id': 1,
            'service_id': 1,
            'doctor_id': 1,
            'appointment_date': datetime.fromisoformat("2023-04-10"),
            'discounted_price': 200,
            'diagnosis_id': None,
            'anamnesis': None,
            'opinion': None,
        },
        {
            'patient_id': 6,
            'visiting_session_id': 2,
            'service_id': 1,
            'doctor_id': 2,
            'appointment_date': datetime.fromisoformat("2024-04-19"),
            'discounted_price': 200,
            'diagnosis_id': None,
            'anamnesis': None,
            'opinion': None,
        },
        {
            'patient_id': 5,
            'visiting_session_id': 1,
            'service_id': 1,
            'doctor_id': 3,
            'appointment_date': datetime.fromisoformat("2023-04-21"),
            'discounted_price': 200,
            'diagnosis_id': 1,
            'anamnesis': None,
            'opinion': None,
        },
        {
            'patient_id': 5,
            'visiting_session_id': 1,
            'service_id': 1,
            'doctor_id': 1,
            'appointment_date': datetime.fromisoformat("2023-04-25"),
            'discounted_price': 200,
            'diagnosis_id': 1,
            'anamnesis': "foo bar baz",
            'opinion': "baz, bar, foo",
        },
    ]
