import pytest

from ..crud.clinic_services import create_clinic_service, read_clinic_services, update_clinic_service


@pytest.fixture()
def setup(db_session, services_clinic):
    for item in services_clinic:
        create_clinic_service(db_session, name=item["name"], price=item["price"])


def test_read_service(db_session, setup, services_clinic):
    result = read_clinic_services(db_session)
    print("result:", result)
    for index, item in enumerate(services_clinic):
        assert result[index].name == item["name"]
        assert result[index].price == item["price"]
        assert result[index].available is True


def test_update_service_price_without_available(db_session, services_clinic, setup):
    result = read_clinic_services(db_session)
    print("result:", result)

    update_clinic_service(db_session, service_id=1, price=300)

    result = read_clinic_services(db_session)
    print("result:", result)
    assert result[0].price == 300
    assert result[0].available is True


def test_update_service_available_without_price(db_session, services_clinic, setup):
    result = read_clinic_services(db_session)
    print("result:", result)

    update_clinic_service(db_session, service_id=1, available=False)

    result = read_clinic_services(db_session)
    print("result:", result)
    assert result[0].price == services_clinic[0]["price"]
    assert result[0].available is False


def test_update_service_price_and_available(db_session, services_clinic, setup):
    result = read_clinic_services(db_session)
    print("result:", result)

    update_clinic_service(db_session, service_id=1, price=300, available=False)

    result = read_clinic_services(db_session)
    print("result:", result)
    assert result[0].price == 300
    assert result[0].available is False


def test_update_service_without_price_and_available(db_session, services_clinic, setup):
    result = read_clinic_services(db_session)
    print("result:", result)

    with pytest.raises(ValueError):
        update_clinic_service(db_session, service_id=1)
