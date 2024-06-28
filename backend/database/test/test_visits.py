from datetime import datetime

import pytest

from database.crud.clinic_services import create_clinic_service
from database.crud.diagnoses import create_diagnosis
from database.crud.doctor_categories import create_doctor_category
from database.crud.doctor_specialities import create_doctor_speciality
from database.crud.doctors import create_doctor
from database.crud.patients import create_patient
from database.crud.patients_categories import create_patient_category
from database.crud.visiting_sessions import create_visiting_session
from database.crud.visits import create_visit, read_visits, update_visit, read_visit_by_id, delete_visit, \
    read_visits_like_doctor


@pytest.fixture()
def create_visits(
        db_session,
        doctors,
        doctor_categories,
        doctor_specialities,
        services_clinic,
        diagnosis,
        visiting_sessions,
        patients,
        visits,
        users,
        patient_categories,
):
    keys_doctor_categories = list(doctor_categories.keys())
    for i in range(3):
        create_doctor_speciality(db_session, doctor_specialities[i])
        create_doctor_category(db_session, doctor_categories[keys_doctor_categories[i]])

        create_clinic_service(
            session=db_session,
            name=services_clinic[i]["name"],
            price=services_clinic[i]["price"],
        )
        create_diagnosis(
            session=db_session,
            name=diagnosis[i]["name"],
        )
        create_visiting_session(
            session=db_session,
            patient_id=visiting_sessions[i]["patient_id"],
        )

    for i in range(len(doctors)):
        create_doctor(
            session=db_session,
            last_name=users[i]["last_name"],
            first_name=users[i]["first_name"],
            middle_name=users[i]["middle_name"],
            hashed_password=users[i]["hashed_password"],
            experience=doctors[i]["experience"],
            speciality_id=doctors[i]["speciality_id"],
            category_id=doctors[i]["category_id"],
        )

    for i in range(len(patients)):
        print("create user id:", i+1)
        create_patient(
            session=db_session,
            last_name=users[i+4]["last_name"],
            first_name=users[i+4]["first_name"],
            middle_name=users[i+4]["middle_name"],
            hashed_password=users[i + 4]["hashed_password"],
            birthday=patients[i]["birthday"],
            category_id=patients[i]["category_id"],
        )

    for item in visits:
        create_visit(
            session=db_session,
            visiting_session_id=item["visiting_session_id"],
            service_id=item["service_id"],
            doctor_id=item["doctor_id"],
            appointment_datetime=item["appointment_date"],
            discounted_price=item["discounted_price"],
            diagnosis_id=item["diagnosis_id"],
            anamnesis=item["anamnesis"],
            opinion=item["opinion"],
        )

    for item in patient_categories:
        create_patient_category(
            session=db_session,
            category=item.name,
            discount_percentage=item.discount_percentage,
        )


def test_read_visits_like_patient(
        db_session,
        create_visits,
        visits,
        visiting_sessions,
):
    for item in visiting_sessions:
        visiting_session_id = item["visiting_session_id"]
        results = read_visits(
            session=db_session,
            visit_session_id=visiting_session_id,
        )

        print('\n', "results:", *results, sep='\n')
        index = 0
        for visit in visits:
            if visit["visiting_session_id"] == visiting_session_id:
                print('index:', index)
                assert results[index]["appointment_datetime"] == visit["appointment_date"]
                assert results[index]["discounted_price"] == visit["discounted_price"]

                index += 1


def test_read_visits_like_doctor(
        db_session,
        create_visits,
        visits,
        doctors,
):
    for item in doctors:
        doctor_id = item["user_id"]
        print("\ndoctor_id:", doctor_id)
        results = read_visits_like_doctor(
            session=db_session,
            doctor_id=doctor_id,
        )

        print('\n', "results:", *results, sep='\n')
        index = 0
        for visit in visits:
            if visit["doctor_id"] == doctor_id:
                print('index:', index)
                assert results[index]["appointment_datetime"] == visit["appointment_date"]
                assert results[index]["discounted_price"] == visit["discounted_price"]
                index += 1


def test_read_visits_like_doctor_detailed(
        db_session,
        create_visits,
        visits,
        doctors,
):
    for item in doctors:
        doctor_id = item["user_id"]
        results = read_visits_like_doctor(
            session=db_session,
            doctor_id=doctor_id,
            detailed_information=True,
        )

        print('\n', "results:", *results, sep='\n')
        index = 0
        for visit in visits:
            if visit["doctor_id"] == doctor_id:
                print('index:', index)
                assert results[index]["appointment_datetime"] == visit["appointment_date"]
                assert results[index]["discounted_price"] == visit["discounted_price"]
                assert results[index]["anamnesis"] == visit["anamnesis"]
                assert results[index]["opinion"] == visit["opinion"]

                index += 1


def test_read_all_visits(
        db_session,
        create_visits,
        visits,
):
    results = read_visits(
        session=db_session,
    )
    print('\n', "results:", *results, sep='\n')

    assert results[0]["appointment_datetime"] == visits[0]["appointment_date"]
    assert results[0]["discounted_price"] == visits[0]["discounted_price"]
    assert len(results) == 6


def test_read_visit_by_id(
        db_session,
        create_visits,
        visits,
):
    visit = read_visit_by_id(
        session=db_session,
        visit_id=1
    )
    print('\n', "results:", visit, sep='\n')

    assert visit[0]["appointment_datetime"] == visits[0]["appointment_date"]
    assert visit[0]["diagnosis_name"] is None
    assert visit[0]["anamnesis"] == visits[0]["anamnesis"]
    assert visit[0]["opinion"] == visits[0]["opinion"]


def test_update_diagnosis_id(db_session, visits, create_visits):
    results = read_visits(session=db_session, detailed_information=True)
    print('\n', "results:", *results, sep='\n')

    update_visit(
        session=db_session,
        visit_id=1,
        diagnosis_id=1
    )

    results = read_visits(session=db_session, detailed_information=True)
    print('\n', "results:", *results, sep='\n')
    assert results[0]["diagnosis_name"] == "foo"


def test_update_anamnesis(db_session, visits, create_visits):
    results = read_visits(session=db_session, detailed_information=True)
    print('\n', "results:", *results, sep='\n')

    new_anamnesis = "bar baz"
    update_visit(
        session=db_session,
        visit_id=1,
        anamnesis=new_anamnesis
    )

    results = read_visits(session=db_session, detailed_information=True)
    print('\n', "results:", *results, sep='\n')
    assert results[0]["anamnesis"] == new_anamnesis


def test_update_opinion(db_session, visits, create_visits):
    results = read_visits(session=db_session, detailed_information=True)
    print('\n', "results:", *results, sep='\n')

    new_opinion = "baz bar"
    update_visit(
        session=db_session,
        visit_id=1,
        opinion=new_opinion,
    )

    results = read_visits(session=db_session, detailed_information=True)
    print('\n', "results:", *results, sep='\n')
    assert results[0]["opinion"] == new_opinion


def test_update_appointment_datetime(db_session, visits, create_visits):
    results = read_visits(session=db_session, detailed_information=True)
    print('\n', "results:", *results, sep='\n')

    new_datetime = datetime.fromisoformat("2023-02-15")
    update_visit(
        session=db_session,
        visit_id=1,
        appointment_datetime=new_datetime
    )

    results = read_visits(session=db_session, detailed_information=True)
    print('\n', "results:", *results, sep='\n')
    assert results[0]["appointment_datetime"] == new_datetime


def test_update_anamnesis_and_diagnosis_id_and_opinion(db_session, visits, create_visits):
    results = read_visits(session=db_session, detailed_information=True)
    print('\n', "results:", *results, sep='\n')

    new_opinion = "baz bar"
    new_anamnesis = "bar baz"
    update_visit(
        session=db_session,
        visit_id=1,
        opinion=new_opinion,
        anamnesis=new_anamnesis,
        diagnosis_id=1
    )

    results = read_visits(session=db_session, detailed_information=True)
    print('\n', "results:", *results, sep='\n')
    assert results[0]["opinion"] == new_opinion
    assert results[0]["anamnesis"] == new_anamnesis
    assert results[0]["diagnosis_name"] == "foo"


def test_delete_visit(db_session, create_visits):
    old_results = read_visits(session=db_session, visit_session_id=1)
    print('\n', "results:", *old_results, sep='\n')

    delete_visit(db_session, visit_id=3)

    new_results = read_visits(session=db_session, visit_session_id=1)
    print('\n', "results:", *new_results, sep='\n')

    assert len(old_results) - len(new_results) == 1
