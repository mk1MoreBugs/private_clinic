from database.crud.patients import create_patient
from database.crud.patients import read_patients
from database.crud.patients_categories import create_patient_category


def test_read_patients(db_session, patients):
    create_patient_category(
        session=db_session,
        category=patients[1]["category_name"],
        discount_percentage=5,
    )
    create_patient(
        session=db_session,
        last_name=patients[0]["last_name"],
        first_name=patients[0]["first_name"],
        middle_name=patients[0]["middle_name"],
        birthday=patients[0]["birthday"],
        hashed_password=patients[0]["hashed_password"],
    )
    create_patient(
        session=db_session,
        last_name=patients[1]["last_name"],
        first_name=patients[1]["first_name"],
        middle_name=patients[1]["middle_name"],
        birthday=patients[1]["birthday"],
        hashed_password=patients[0]["hashed_password"],
        category_id=1,
    )
    create_patient(
        session=db_session,
        last_name=patients[2]["last_name"],
        first_name=patients[2]["first_name"],
        middle_name=patients[2]["middle_name"],
        birthday=patients[2]["birthday"],
        hashed_password=patients[0]["hashed_password"],
        category_id=None,
    )

    result = read_patients(session=db_session)

    print("result:", result)
    for index, item in enumerate(patients):
        assert result[index]["last_name"] == item["last_name"]
        assert result[index]["first_name"] == item["first_name"]
        assert result[index]["middle_name"] == item["middle_name"]
        assert result[index]["birthday"] == item["birthday"]

    assert result[0]["category_name"] is None
    assert result[0]["category_id"] is None
    assert result[1]["category_name"] == patients[1]["category_name"]
    assert result[1]["category_id"] == 1
