
from unittest.mock import Mock
import pytest

from services.employee_service import EmployeeService
from models.employee import Employee


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def employee_service(mock_repository):
    return EmployeeService(mock_repository)


@pytest.fixture
def employee():
    return Employee(
        id_employee=1,
        first_name="Theo",
        last_name="Macrez",
        email="theo@test.com",
        phone="+33600000000",
        birth_date="1995-03-04"
    )


def test_get_employee_by_id_should_return_employee(
        employee_service,
        mock_repository,
        employee):

    mock_repository.find_by_id.return_value = employee

    result = employee_service.get_employee_by_id(1)

    assert result == employee

    mock_repository.find_by_id.assert_called_once_with(1)


def test_get_employee_by_id_should_return_none_when_not_found(
        employee_service,
        mock_repository):

    mock_repository.find_by_id.return_value = None

    result = employee_service.get_employee_by_id(999)

    assert result is None

    mock_repository.find_by_id.assert_called_once_with(999)


def test_create_employee_should_create_employee_when_email_is_unique(
        employee_service,
        mock_repository,
        employee):

    mock_repository.find_by_email.return_value = None
    mock_repository.create.return_value = employee

    result = employee_service.create_employee(
        "Theo",
        "Macrez",
        "theo@test.com",
        "+33600000000",
        "1995-03-04"
    )

    assert result == employee

    mock_repository.find_by_email.assert_called_once_with(
        "theo@test.com"
    )

    mock_repository.create.assert_called_once_with(
        "Theo",
        "Macrez",
        "theo@test.com",
        "+33600000000",
        "1995-03-04"
    )


def test_create_employee_should_raise_exception_when_email_already_exists(
        employee_service,
        mock_repository,
        employee):

    mock_repository.find_by_email.return_value = employee

    with pytest.raises(ValueError, match="Email already exists"):
        employee_service.create_employee(
            "Theo",
            "Macrez",
            "theo@test.com",
            "+33600000000",
            "1995-03-04"
        )

    mock_repository.create.assert_not_called()


def test_update_employee_should_call_repository(
        employee_service,
        mock_repository,
        employee):

    mock_repository.update.return_value = employee

    result = employee_service.update_employee(
        "Theo",
        "Macrez",
        "theo@test.com",
        "+33600000000",
        "1995-03-04",
        1
    )

    assert result == employee

    mock_repository.update.assert_called_once_with(
        "Theo",
        "Macrez",
        "theo@test.com",
        "+33600000000",
        "1995-03-04",
        1
    )


def test_delete_employee_should_return_true_when_deleted(
        employee_service,
        mock_repository):

    mock_repository.delete.return_value = True

    result = employee_service.delete_employee(1)

    assert result is True

    mock_repository.delete.assert_called_once_with(1)


def test_delete_employee_should_return_false_when_not_deleted(
        employee_service,
        mock_repository):

    mock_repository.delete.return_value = False

    result = employee_service.delete_employee(999)

    assert result is False

    mock_repository.delete.assert_called_once_with(999)