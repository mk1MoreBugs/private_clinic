from database.crud.doctors import create_doctor, read_doctor_by_id
from database.crud.patients import read_patient_by_id, create_patient
from database.crud.users import create_user_and_commit, read_users, read_hashed_password, update_hashed_password


def test_create_and_read_users(
        db_session,
        users,
):
    for item in users:
        create_user_and_commit(
            session=db_session,
            last_name=item["last_name"],
            first_name=item["first_name"],
            middle_name=item["middle_name"],
            hashed_password=item["hashed_password"],
        )

    result = read_users(session=db_session)
    assert len(result) == len(users)
    for index, item in enumerate(users):
        assert result[index].last_name == item["last_name"]
        assert result[index].first_name == item["first_name"]
        assert result[index].middle_name == item["middle_name"]
        assert result[index].hashed_password == item["hashed_password"]


def test_create_user_and_read_hashed_password(db_session, users):
    hashed_password = "top_secret"
    for index, item in enumerate(users):
        create_user_and_commit(
            session=db_session,
            last_name=item["last_name"],
            first_name=item["first_name"],
            middle_name=item["middle_name"],
            # create unique password for all mock users
            hashed_password=f"{hashed_password} {index}",
        )

    result_hashed_pass = read_hashed_password(
        session=db_session,
        user_id=1,
    )
    print(result_hashed_pass)
    assert result_hashed_pass == f"{hashed_password} 0"


def test_create_user_and_update_hashed_password(db_session, users):
    hashed_password = "top_secret"
    update_password = "update_top_secret"
    create_user_and_commit(
        session=db_session,
        last_name=users[0]["last_name"],
        first_name=users[0]["first_name"],
        middle_name=users[0]["middle_name"],
        hashed_password=hashed_password,
    )

    update_hashed_password(
        session=db_session,
        user_id=1,
        new_hashed_password=update_password
    )

    result_hashed_pass = read_hashed_password(
        session=db_session,
        user_id=1,
    )
    print(result_hashed_pass)
    assert result_hashed_pass == update_password


def test_verify_user_role_with_doctor_entry_in_the_database(
        db_session,
        users,
        doctors,
):
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

    patient = read_patient_by_id(
        session=db_session,
        user_id=1
    )
    doctor = read_doctor_by_id(
        session=db_session,
        user_id=1
    )
    print(patient)

    assert patient is None
    assert doctor.user_id == 1


def test_verify_user_role_with_patient_entry_in_the_database(
        db_session,
        users,
        patients,
):
    create_patient(
        session=db_session,
        last_name=users[4]["last_name"],
        first_name=users[4]["first_name"],
        middle_name=users[4]["middle_name"],
        hashed_password=users[4]["hashed_password"],
        birthday=patients[0]["birthday"],
    )

    patient = read_patient_by_id(
        session=db_session,
        user_id=1
    )
    print(patient)

    doctor = read_doctor_by_id(
        session=db_session,
        user_id=1
    )
    print(patient)

    assert patient.user_id == 1
    assert doctor is None
