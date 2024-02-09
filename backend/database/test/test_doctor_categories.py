import pytest

from ..crud.doctor_categories import create_doctor_category, read_doctor_category


def test_create_invalid_category(db_session):
    with pytest.raises(LookupError):
        create_doctor_category(db_session, "bar")
        read_doctor_category(db_session)


def test_read_doctor_category(db_session, doctor_categories):
    for key in doctor_categories:
        create_doctor_category(db_session, key)

    result = read_doctor_category(db_session)

    print("result:", result)
    for index, key in enumerate(doctor_categories):
        assert result[index].name == doctor_categories[key]
