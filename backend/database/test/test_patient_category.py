import pytest

from ..crud.patients_categories import create_patient_category, read_patient_categories
from ..crud.patients_categories import read_patient_categories_by_visiting_session_id
from ..crud.visiting_sessions import create_visiting_session
from ..crud.patients import create_patient


def test_read_patient_categories(db_session, patient_categories):
    for item in patient_categories:
        create_patient_category(
            session=db_session,
            category=item.name,
            discount_percentage=item.discount_percentage,
        )
    result = read_patient_categories(session=db_session)

    print("result:", result)
    for index, item in enumerate(patient_categories):
        assert result[index].name == item.name
        assert result[index].discount_percentage == item.discount_percentage


def test_read_patient_categories_by_visiting_id_return_10(db_session, patient_categories, patients, users):
    create_patient_category(
        session=db_session,
        category="foo",
        discount_percentage=10,
    )
    create_patient(
        session=db_session,
        last_name=users[0]["last_name"],
        first_name=users[0]["first_name"],
        middle_name=users[0]["middle_name"],
        hashed_password=users[0]["hashed_password"],
        birthday=patients[0]["birthday"],
        category_id=1,
    )
    create_visiting_session(db_session, patient_id=1)

    result = read_patient_categories_by_visiting_session_id(session=db_session, visiting_session_id=1)

    print("result:", result)
    assert result == 10


def test_read_patient_categories_by_visiting_id_return_none(db_session, patient_categories, patients, users):
    create_patient_category(
        session=db_session,
        category="foo",
        discount_percentage=10,
    )
    create_patient(
        session=db_session,
        last_name=users[0]["last_name"],
        first_name=users[0]["first_name"],
        middle_name=users[0]["middle_name"],
        hashed_password=users[0]["hashed_password"],
        birthday=patients[0]["birthday"],
        category_id=None,
    )
    create_visiting_session(db_session, patient_id=1)

    result = read_patient_categories_by_visiting_session_id(session=db_session, visiting_session_id=1)

    print("result:", result)
    assert result is None
