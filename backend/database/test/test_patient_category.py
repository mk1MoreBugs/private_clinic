import pytest

from ..crud.patients_categories import create_patient_category, read_patient_categories
from ..models.patient_category import PatientCategory


@pytest.fixture()
def patient_categories():
    return [
        PatientCategory(
            category="test category",
            discount_percentage=10,
        ),
        PatientCategory(
            category="test category 2",
            discount_percentage=25,
        ),
    ]


def test_read_patient_categories(db_session, patient_categories):
    for item in patient_categories:
        create_patient_category(
            session=db_session,
            category=item.category,
            discount_percentage=item.discount_percentage,
        )
    result = read_patient_categories(session=db_session)

    print("result:", result)
    for index, item in enumerate(patient_categories):
        assert result[index].category == item.category
        assert result[index].discount_percentage == item.discount_percentage
