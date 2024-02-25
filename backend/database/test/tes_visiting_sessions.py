from datetime import datetime

from database.crud.visiting_sessions import create_visiting_session, read_visiting_session
from database.crud.visits import create_visit


def test_read_visiting_session_when_visits_not_exist(db_session):
    patient_id = 1
    create_visiting_session(db_session, patient_id=patient_id)

    result = read_visiting_session(db_session, patient_id=patient_id)
    print("\n", "patient_id:", patient_id, "result:", result, "\n")

    assert result[0]["session_id"] == 1


def test_read_visiting_session_when_visits_is_exist(db_session, visits):
    create_visiting_session(db_session, patient_id=1)
    create_visiting_session(db_session, patient_id=1)
    create_visiting_session(db_session, patient_id=2)
    for item in visits:
        create_visit(
            session=db_session,
            visiting_session_id=item["visiting_session_id"],
            service_id=item["service_id"],
            doctor_id=item["doctor_id"],
            appointment_datetime=item["appointment_date"],
            discounted_price=item["discounted_price"],
        )

    patient_id = 1
    result = read_visiting_session(db_session, patient_id=patient_id)
    print("\n", "patient_id:", patient_id, "result:", result, "\n")

    assert result[0]["date_start"] == datetime.fromisoformat("2023-04-10")
    assert result[0]["date_end"] == datetime.fromisoformat("2023-04-25")
    assert result[0]["sum_price"] == 3 * 200

    assert result[1]["date_start"] == datetime.fromisoformat("2024-04-19")
    assert result[1]["date_end"] == datetime.fromisoformat("2024-04-19")
    assert result[1]["sum_price"] == 200

    patient_id = 2
    result = read_visiting_session(db_session, patient_id=patient_id)
    print("\n", "patient_id:", patient_id, "result:", result, "\n")
    assert result[0]["date_start"] == datetime.fromisoformat("2023-03-15")
    assert result[0]["date_end"] == datetime.fromisoformat("2023-03-20")
    assert result[0]["sum_price"] == 800 + 250
