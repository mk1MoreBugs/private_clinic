from ..crud.diagnoses import create_diagnosis, read_diagnoses


def test_read_diagnosis(db_session, diagnosis):
    for item in diagnosis:
        create_diagnosis(db_session, item["name"])

    result = read_diagnoses(db_session)
    print("result:", result)
    for index, item in enumerate(diagnosis):
        assert result[index].name == item["name"]
