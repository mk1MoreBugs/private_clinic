from ..crud.doctor_specialities import create_doctor_speciality, read_doctor_speciality


def test_read_doctor_speciality(db_session, doctor_specialities):
    for item in doctor_specialities:
        create_doctor_speciality(db_session, item)

    result = read_doctor_speciality(db_session)

    print("result:", result)
    for index, item in enumerate(doctor_specialities):
        assert result[index].name == item
