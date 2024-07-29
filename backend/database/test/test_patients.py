from database.crud.patients import create_patient
from database.crud.patients import read_patients
from database.crud.patients_categories import create_patient_category


def test_read_patients(db_session, patients, users):
    create_patient_category(
        session=db_session,
        category=patients[1]["category_name"],
        discount_percentage=5,
    )
    create_patient(
        session=db_session,
        last_name=users[4]["last_name"],
        first_name=users[4]["first_name"],
        middle_name=users[4]["middle_name"],
        hashed_password=users[4]["hashed_password"],
        birthday=patients[0]["birthday"],
    )
    create_patient(
        session=db_session,
        last_name=users[5]["last_name"],
        first_name=users[5]["first_name"],
        middle_name=users[5]["middle_name"],
        hashed_password=users[5]["hashed_password"],
        birthday=patients[1]["birthday"],
        category_id=1,
    )
    create_patient(
        session=db_session,
        last_name=users[6]["last_name"],
        first_name=users[6]["first_name"],
        middle_name=users[6]["middle_name"],
        hashed_password=users[6]["hashed_password"],
        birthday=patients[2]["birthday"],
        category_id=None,
    )

    result = read_patients(session=db_session)

    print("result:", result)
    for index, item in enumerate(result):
        assert item["last_name"] == users[index+4]["last_name"]
        assert item["first_name"] == users[index+4]["first_name"]
        assert item["middle_name"] == users[index+4]["middle_name"]
        assert result[index]["birthday"] == item["birthday"]

    assert result[0]["category_name"] is None
    assert result[0]["category_id"] is None
    assert result[1]["category_name"] == patients[1]["category_name"]
    assert result[1]["category_id"] == 1
