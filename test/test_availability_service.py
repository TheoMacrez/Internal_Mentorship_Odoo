from datetime import time
from unittest.mock import Mock
import pytest

from services.availability_service import AvailabilityService
from models.availability import Availability
from models.employee import Employee


@pytest.fixture
def availability_repository():
    return Mock()


@pytest.fixture
def employee_repository():
    return Mock()


@pytest.fixture
def availability_service(availability_repository, employee_repository):
    return AvailabilityService(availability_repository, employee_repository)


@pytest.fixture(autouse=True)
def mock_get_connection(patch_get_connection):
    return patch_get_connection("services.availability_service.get_connection")


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


@pytest.fixture
def availability():
    return Availability(
        id_availability=1,
        day_of_week="MONDAY",
        start_time=time(9, 0),
        end_time=time(12, 0),
        employee_id=1
    )


def test_get_availability_by_id_should_return_availability(
        availability_service,
        availability_repository,
        availability):

    availability_repository.find_by_id.return_value = availability

    result = availability_service.get_availability_by_id(1)

    assert result == availability
    availability_repository.find_by_id.assert_called_once_with(1)


def test_get_all_availabilities_should_return_availabilities(
        availability_service,
        availability_repository,
        availability):

    availability_repository.find_all.return_value = [availability]

    result = availability_service.get_all_availabilities()

    assert result == [availability]
    availability_repository.find_all.assert_called_once_with()


def test_get_availability_by_id_should_return_none_when_not_found(
        availability_service,
        availability_repository):

    availability_repository.find_by_id.return_value = None

    result = availability_service.get_availability_by_id(999)

    assert result is None
    availability_repository.find_by_id.assert_called_once_with(999)


def test_get_availabilities_by_employee_id_should_return_availabilities(
        availability_service,
        availability_repository,
        employee_repository,
        employee,
        availability,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    availability_repository.find_by_employee_id.return_value = [availability]

    result = availability_service.get_availabilities_by_employee_id(1)

    assert result == [availability]
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    availability_repository.find_by_employee_id.assert_called_once_with(
        1,
        fake_connection
    )


def test_get_availabilities_by_employee_id_should_raise_error_when_employee_not_found(
        availability_service,
        availability_repository,
        employee_repository,
        fake_connection):

    employee_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Employee does not exist"):
        availability_service.get_availabilities_by_employee_id(999)

    employee_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    availability_repository.find_by_employee_id.assert_not_called()


def test_get_availabilities_by_day_of_week_should_return_availabilities(
        availability_service,
        availability_repository,
        availability):

    availability_repository.find_by_day_of_week.return_value = [availability]

    result = availability_service.get_availabilities_by_day_of_week("MONDAY")

    assert result == [availability]
    availability_repository.find_by_day_of_week.assert_called_once_with("MONDAY")


def test_get_availabilities_covering_time_interval_should_return_availabilities(
        availability_service,
        availability_repository,
        availability):

    availability_repository.find_covering_time_interval.return_value = [availability]

    result = availability_service.get_availabilities_covering_time_interval(
        "MONDAY",
        time(10, 0),
        time(11, 0)
    )

    assert result == [availability]
    availability_repository.find_covering_time_interval.assert_called_once_with(
        "MONDAY",
        time(10, 0),
        time(11, 0)
    )


def test_get_availabilities_covering_time_interval_should_raise_error_when_time_interval_is_invalid(
        availability_service,
        availability_repository):

    with pytest.raises(ValueError, match="Start time must be before end time"):
        availability_service.get_availabilities_covering_time_interval(
            "MONDAY",
            time(12, 0),
            time(9, 0)
        )

    availability_repository.find_covering_time_interval.assert_not_called()


def test_create_availability_should_create_when_employee_exists(
        availability_service,
        availability_repository,
        employee_repository,
        employee,
        availability,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    availability_repository.create_availability.return_value = availability

    result = availability_service.create_availability(
        "MONDAY",
        time(9, 0),
        time(12, 0),
        1
    )

    assert result == availability
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    availability_repository.create_availability.assert_called_once_with(
        "MONDAY",
        time(9, 0),
        time(12, 0),
        1,
        fake_connection
    )


def test_create_availability_should_raise_error_when_employee_not_found(
        availability_service,
        availability_repository,
        employee_repository,
        fake_connection):

    employee_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Employee does not exist"):
        availability_service.create_availability(
            "MONDAY",
            time(9, 0),
            time(12, 0),
            999
        )

    employee_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    availability_repository.create_availability.assert_not_called()


def test_create_availability_should_raise_error_when_time_interval_is_invalid(
        availability_service,
        availability_repository,
        employee_repository):

    with pytest.raises(ValueError, match="Start time must be before end time"):
        availability_service.create_availability(
            "MONDAY",
            time(12, 0),
            time(9, 0),
            1
        )

    employee_repository.find_by_id.assert_not_called()
    availability_repository.create_availability.assert_not_called()


def test_update_availability_should_call_repository_when_employee_exists(
        availability_service,
        availability_repository,
        employee_repository,
        employee,
        availability,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    availability_repository.update_availability.return_value = availability

    result = availability_service.update_availability(
        1,
        "MONDAY",
        time(9, 0),
        time(12, 0),
        1
    )

    assert result == availability
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    availability_repository.update_availability.assert_called_once_with(
        1,
        "MONDAY",
        time(9, 0),
        time(12, 0),
        1,
        fake_connection
    )


def test_update_availability_should_raise_error_when_employee_not_found(
        availability_service,
        availability_repository,
        employee_repository,
        fake_connection):

    employee_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Employee does not exist"):
        availability_service.update_availability(
            1,
            "MONDAY",
            time(9, 0),
            time(12, 0),
            999
        )

    employee_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    availability_repository.update_availability.assert_not_called()


def test_update_availability_should_raise_error_when_time_interval_is_invalid(
        availability_service,
        availability_repository,
        employee_repository):

    with pytest.raises(ValueError, match="Start time must be before end time"):
        availability_service.update_availability(
            1,
            "MONDAY",
            time(9, 0),
            time(9, 0),
            1
        )

    employee_repository.find_by_id.assert_not_called()
    availability_repository.update_availability.assert_not_called()


def test_delete_availability_should_return_true_when_deleted(
        availability_service,
        availability_repository):

    availability_repository.delete_availability.return_value = True

    result = availability_service.delete_availability(1)

    assert result is True
    availability_repository.delete_availability.assert_called_once_with(1)


def test_delete_availability_should_return_false_when_not_deleted(
        availability_service,
        availability_repository):

    availability_repository.delete_availability.return_value = False

    result = availability_service.delete_availability(999)

    assert result is False
    availability_repository.delete_availability.assert_called_once_with(999)
