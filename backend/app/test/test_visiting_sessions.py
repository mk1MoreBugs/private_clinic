from fastapi import status


PATH_URL = "/session"


def test_create_and_read_visiting_sessions(client):
    created = client.post(
        url=PATH_URL+"/create",
        json=1,
    )

    assert created.status_code == status.HTTP_201_CREATED


def test_read_visits(client):
    response = client.get(PATH_URL + "/0")
    print('\n', response.json())

    assert response.status_code == status.HTTP_200_OK
