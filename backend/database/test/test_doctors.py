import pytest

from database.crud.doctor_categories import create_doctor_category
from database.crud.doctor_specialities import create_doctor_speciality
from database.crud.doctors import create_doctor, read_doctors, quit_doctor


@pytest.fixture()
def create_fake_doctor(db_session, users, doctors):
    create_doctor(
        session=db_session,
        last_name=users[0]["last_name"],
        first_name=users[0]["first_name"],
        middle_name=users[0]["middle_name"],
        hashed_password=users[0]["hashed_password"],
        experience=doctors[0]["experience"],
        speciality_id=doctors[0]["speciality_id"],
        category_id=doctors[0]["category_id"],
    )


def test_read_doctor(
        db_session,
        doctors,
        doctor_categories,
        doctor_specialities,
        users,
        create_fake_doctor,
):
    create_doctor_category(db_session, doctor_categories["highest"])
    create_doctor_speciality(db_session, doctor_specialities[0])

    result = read_doctors(session=db_session)
    print("result:", result)
    assert result[0]["last_name"] == users[0]["last_name"]
    assert result[0]["first_name"] == users[0]["first_name"]
    assert result[0]["middle_name"] == users[0]["middle_name"]
    assert result[0]["experience"] == doctors[0]["experience"]
    assert result[0]["category_name"] == doctor_categories["highest"]
    assert result[0]["speciality_name"] == doctor_specialities[0]
    assert result[0]["quit_clinic"] is False


def test_quit_doctor(db_session, doctors, create_fake_doctor):
    quit_doctor(db_session, 1)
    result = read_doctors(session=db_session)
    print("result:", result)
    assert result[0]["quit_clinic"] is True
