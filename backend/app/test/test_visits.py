from datetime import datetime

from fastapi import status
import pytest

PATH_URL = "/visits"


@pytest.fixture()
def visit():
    return {
            'visiting_session_id': 3,
            'service_id': 1,
            'doctor_id': 3,
            'appointment_datetime': "2024-02-10T00:03:55.833Z",
            'discounted_price': 800,
            'diagnosis_id': 1,
        }


def test_read_visits(client):
    response = client.get(
        url=PATH_URL+"/1",
    )
    print(response.json())
    assert response.status_code == status.HTTP_200_OK


def test_create_visit(client, visit):
    create = client.post(
        url=PATH_URL+"/",
        json=visit,
    )

    assert create.status_code == status.HTTP_201_CREATED


def test_update_visit(client, visit):
    create = client.post(
        url=PATH_URL + "/",
        json=visit,
    )
    update = client.put(
        url=PATH_URL + "/update/1",
        json={
            'anamnesis': "bar bar",
            'opinion': "bar",
        },
    )
    response = client.get(PATH_URL + "/1")
    print("test")
    print('\n', response.json())

    assert create.status_code == status.HTTP_201_CREATED
    assert update.status_code == status.HTTP_200_OK
    assert response.status_code == status.HTTP_200_OK


def test_delete_visit(client, visit):
    create = client.post(
        url=PATH_URL + "/",
        json=visit,
    )
    delete = client.delete(PATH_URL + "/delete/1")
    response = client.get(PATH_URL + "/1")

    assert create.status_code == status.HTTP_201_CREATED
    assert delete.status_code == status.HTTP_200_OK
    assert response.status_code == status.HTTP_200_OK
