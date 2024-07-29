from datetime import date
import pytest
from fastapi import status
from app.schemas.patient import PatientIn

PATH_URL = "/patients"


@pytest.fixture()
def patients():
    return [
        {
            "last_name": "Иванов1",
            "first_name": "Иван1",
            "middle_name": "Иванович1",
            "birthday": "1999-12-04",
            "category_id": 1,
            "hashed_password": "",
        },
        {
            "last_name": "Иванов2",
            "first_name": "Иван2",
            "middle_name": "Иванович2",
            "birthday": "1995-12-10",
            "category_id": None,
            "hashed_password": "",
        },
    ]


def test_create_patients(patients):
    for item in patients:
        patient = PatientIn(**item)

        print(patient)
        dict_patient = dict(patient)
        dict_patient["birthday"] = date.strftime(dict_patient["birthday"], '%Y-%m-%d')
        assert item == dict_patient


def test_create_and_read_patients(client, patients):
    before = client.get(PATH_URL + "/")
    print('\n', before.json())

    created = client.post(
        PATH_URL+"/",
        json=patients[0]
    )

    after = client.get(PATH_URL + "/")
    print('\n', after.json())
    assert len(after.json()) - len(before.json()) == 1
    assert before.status_code == status.HTTP_200_OK
    assert created.status_code == status.HTTP_201_CREATED


def test_read_visiting_sessions_by_patient_id(client, patients):
    response = client.get(PATH_URL + "/0")
    print('\n', response.json())

    assert response.status_code == status.HTTP_200_OK


def test_create_and_read_patients_unprocessable_entity(client, patients):
    created = client.post(
        PATH_URL+"/",
        json={
            "last_name": "Иванов1",
            "first_name": "Иван1",
            "middle_name": "Иванович1",
            "birthday": "1999-12-04",
            "category_id": "1f"
        }
    )
    assert created.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
