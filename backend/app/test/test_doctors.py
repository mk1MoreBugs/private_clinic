import pytest
from fastapi import status

from app.schemas.doctor import DoctorIn

PATH_URL = "/doctors"


@pytest.fixture()
def doctors():
    return [
        {
            "last_name": "Фамилия",
            "first_name": "Имя",
            "middle_name": "Отчество",
            "experience": 10,
            "speciality_id": 1,
            "category_id": 1,
            "hashed_password": "",
        },
        {
            "last_name": "Фамилия2",
            "first_name": "Имя",
            "middle_name": "Отчество",
            "experience": 5,
            "speciality_id": 2,
            "category_id": 2,
            "hashed_password": "",
        },
        {
            "last_name": "Фамилия2",
            "first_name": "Имя",
            "middle_name": "Отчество",
            "experience": 15,
            "speciality_id": 3,
            "category_id": 3,
            "hashed_password": "",
        },
    ]


def test_create_doctor(doctors):
    for item in doctors:
        doctor = DoctorIn(**item)

        print(doctor)
        assert item == dict(doctor)


def test_create_and_read_doctors(client, doctors):
    before = client.get(PATH_URL + "/")
    print('\n', before.json())

    created = client.post(
        PATH_URL+"/",
        json=doctors[0]
    )

    after = client.get(PATH_URL + "/")
    print('\n', after.json())
    assert len(after.json()) - len(before.json()) == 1
    assert before.status_code == status.HTTP_200_OK
    assert created.status_code == status.HTTP_201_CREATED


def test_read_visits_by_doctor_id(client, doctors):
    response = client.get(PATH_URL + "/0")
    print('\n', response.json())

    assert response.status_code == status.HTTP_200_OK

