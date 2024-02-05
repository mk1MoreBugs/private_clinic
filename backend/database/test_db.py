from datetime import date

import pytest

from database.crud import create_patient_categories, read_patient_categories, create_patient, read_patient, \
    create_doctor_speciality, read_doctor_speciality, create_service, read_service, update_service, create_diagnosis, \
    read_diagnoses, create_visiting_session, read_visiting_session, read_visiting_session_by_patient_id
from database.database import create_db
from database.models.base import Base
from database.models.doctor_speciality import Speciality
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



@pytest.fixture(scope="module")
def doctor_specialities():
    return ["foo", "bar", "baz"]


@pytest.fixture(scope="module")
def doctor_categories():
    return ["foo", "bar", "baz"]


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
def diagnosis():
    return [
        {"name": "foo"},
        {"name": "bar"},
        {"name": "baz"},
    ]


@pytest.fixture(scope="module")
def list_of_patient_id():
    return list(range(1, 6))


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


def test_create_doctor_speciality(db_session, doctor_specialities):
    for item in doctor_specialities:
        create_doctor_speciality(db_session, item)

    result = read_doctor_speciality(db_session)

    print("result:", result)
    for index, item in enumerate(doctor_specialities):
        assert result[index].name == item


def test_create_doctor_category(db_session, doctor_categories):
    for item in doctor_categories:
        create_doctor_speciality(db_session, item)

    result = read_doctor_speciality(db_session)

    print("result:", result)
    for index, item in enumerate(doctor_categories):
        assert result[index].name == item


def test_create_service(db_session, services_clinic):
    for item in services_clinic:
        create_service(db_session, name=item["name"], price=item["price"])

    result = read_service(db_session)
    print("result:", result)
    for index, item in enumerate(services_clinic):
        assert result[index].name == item["name"]
        assert result[index].price == item["price"]
        assert result[index].available is True


def test_update_service(db_session, services_clinic):
    for item in services_clinic:
        create_service(db_session, name=item["name"], price=item["price"])

    result = read_service(db_session)
    print("result:", result)

    update_service(db_session, service_id=1, price=300)
    update_service(db_session, service_id=2, available=False)
    update_service(db_session, service_id=3, price=1300, available=False)

    result = read_service(db_session)
    print("result:", result)
    assert result[0].price == 300
    assert result[0].available is True

    assert result[1].price == services_clinic[1]["price"]
    assert result[1].available is False

    assert result[2].price == 1300
    assert result[2].available is False

    with pytest.raises(ValueError):
        update_service(db_session, service_id=1)


def test_create_diagnosis(db_session, diagnosis):
    for item in diagnosis:
        create_diagnosis(db_session, item["name"])

    result = read_diagnoses(db_session)
    print("result:", result)
    for index, item in enumerate(diagnosis):
        assert result[index].name == item["name"]


def test_create_visiting_session(db_session, list_of_patient_id):

    for patient_id in list_of_patient_id:
        create_visiting_session(db_session, patient_id=patient_id)

    result = read_visiting_session(db_session)

    for index, patient_id in enumerate(list_of_patient_id):
        assert result[index].patient_id == patient_id


def test_create_visiting_session_by_patient_id(db_session, list_of_patient_id):
    for patient_id in list_of_patient_id:
        create_visiting_session(db_session, patient_id=patient_id)
    create_visiting_session(db_session, patient_id=1)
    create_visiting_session(db_session, patient_id=1)

    result = read_visiting_session_by_patient_id(db_session, patient_id=1)
    print("result:", result)

    assert result[0].patient_id == 1
    assert result[0].patient_id != 2
    assert result[1].patient_id != 2
    assert result[2].patient_id != 2
