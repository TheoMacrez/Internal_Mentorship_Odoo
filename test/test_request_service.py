from unittest.mock import Mock
import pytest

from models.employee import Employee
from models.request import Request
from models.skill import Skill
from services.request_service import RequestService


@pytest.fixture
def request_repository():
    return Mock()


@pytest.fixture
def employee_repository():
    return Mock()


@pytest.fixture
def skill_repository():
    return Mock()


@pytest.fixture
def request_service(request_repository, employee_repository, skill_repository):
    return RequestService(
        request_repository,
        employee_repository,
        skill_repository
    )


@pytest.fixture(autouse=True)
def mock_get_connection(patch_get_connection):
    return patch_get_connection("services.request_service.get_connection")


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
def skill():
    return Skill(
        id_skill=1,
        name="PostgreSQL",
        skill_type="TECHNICAL"
    )


@pytest.fixture
def mentorship_request():
    return Request(
        id_request=1,
        start_level=2,
        target_level=4,
        employee_id=1,
        skill_id=1
    )


def test_get_all_requests_should_return_requests(
        request_service,
        request_repository,
        mentorship_request):

    request_repository.find_all.return_value = [mentorship_request]

    result = request_service.get_all_requests()

    assert result == [mentorship_request]
    request_repository.find_all.assert_called_once_with()


def test_get_request_by_id_should_return_request(
        request_service,
        request_repository,
        mentorship_request):

    request_repository.find_by_id.return_value = mentorship_request

    result = request_service.get_request_by_id(1)

    assert result == mentorship_request
    request_repository.find_by_id.assert_called_once_with(1)


def test_get_request_by_id_should_return_none_when_not_found(
        request_service,
        request_repository):

    request_repository.find_by_id.return_value = None

    result = request_service.get_request_by_id(999)

    assert result is None
    request_repository.find_by_id.assert_called_once_with(999)


def test_get_requests_by_employee_id_should_return_requests(
        request_service,
        request_repository,
        employee_repository,
        employee,
        mentorship_request,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    request_repository.find_by_employee_id.return_value = [mentorship_request]

    result = request_service.get_requests_by_employee_id(1)

    assert result == [mentorship_request]
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    request_repository.find_by_employee_id.assert_called_once_with(
        1,
        fake_connection
    )


def test_get_requests_by_employee_id_should_raise_error_when_employee_not_found(
        request_service,
        request_repository,
        employee_repository,
        fake_connection):

    employee_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Employee does not exist"):
        request_service.get_requests_by_employee_id(999)

    employee_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    request_repository.find_by_employee_id.assert_not_called()


def test_get_requests_by_skill_id_should_return_requests(
        request_service,
        request_repository,
        skill_repository,
        skill,
        mentorship_request,
        fake_connection):

    skill_repository.find_by_id.return_value = skill
    request_repository.find_by_skill_id.return_value = [mentorship_request]

    result = request_service.get_requests_by_skill_id(1)

    assert result == [mentorship_request]
    skill_repository.find_by_id.assert_called_once_with(1, fake_connection)
    request_repository.find_by_skill_id.assert_called_once_with(
        1,
        fake_connection
    )


def test_get_requests_by_skill_id_should_raise_error_when_skill_not_found(
        request_service,
        request_repository,
        skill_repository,
        fake_connection):

    skill_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Skill does not exist"):
        request_service.get_requests_by_skill_id(999)

    skill_repository.find_by_id.assert_called_once_with(999, fake_connection)
    request_repository.find_by_skill_id.assert_not_called()


def test_get_requests_by_start_level_should_return_requests(
        request_service,
        request_repository,
        mentorship_request):

    request_repository.find_by_start_level.return_value = [mentorship_request]

    result = request_service.get_requests_by_start_level(2)

    assert result == [mentorship_request]
    request_repository.find_by_start_level.assert_called_once_with(2)


def test_get_requests_by_start_level_should_raise_error_when_level_is_invalid(
        request_service,
        request_repository):

    with pytest.raises(ValueError, match="Level must be between 1 and 5"):
        request_service.get_requests_by_start_level(6)

    request_repository.find_by_start_level.assert_not_called()


def test_get_requests_by_target_level_should_return_requests(
        request_service,
        request_repository,
        mentorship_request):

    request_repository.find_by_target_level.return_value = [mentorship_request]

    result = request_service.get_requests_by_target_level(4)

    assert result == [mentorship_request]
    request_repository.find_by_target_level.assert_called_once_with(4)


def test_get_requests_by_target_level_should_raise_error_when_level_is_invalid(
        request_service,
        request_repository):

    with pytest.raises(ValueError, match="Level must be between 1 and 5"):
        request_service.get_requests_by_target_level(0)

    request_repository.find_by_target_level.assert_not_called()


def test_get_requests_by_employee_id_and_skill_id_should_return_requests(
        request_service,
        request_repository,
        employee_repository,
        skill_repository,
        employee,
        skill,
        mentorship_request,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    skill_repository.find_by_id.return_value = skill
    request_repository.find_by_employee_id_and_skill_id.return_value = [mentorship_request]

    result = request_service.get_requests_by_employee_id_and_skill_id(1, 1)

    assert result == [mentorship_request]
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    skill_repository.find_by_id.assert_called_once_with(1, fake_connection)
    request_repository.find_by_employee_id_and_skill_id.assert_called_once_with(
        1,
        1,
        fake_connection
    )


def test_create_request_should_create_when_valid(
        request_service,
        request_repository,
        employee_repository,
        skill_repository,
        employee,
        skill,
        mentorship_request,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    skill_repository.find_by_id.return_value = skill
    request_repository.create.return_value = mentorship_request

    result = request_service.create_request(2, 4, 1, 1)

    assert result == mentorship_request
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    skill_repository.find_by_id.assert_called_once_with(1, fake_connection)
    request_repository.create.assert_called_once_with(
        2,
        4,
        1,
        1,
        fake_connection
    )


def test_create_request_should_raise_error_when_level_is_invalid(
        request_service,
        request_repository,
        employee_repository,
        skill_repository):

    with pytest.raises(ValueError, match="Level must be between 1 and 5"):
        request_service.create_request(0, 4, 1, 1)

    employee_repository.find_by_id.assert_not_called()
    skill_repository.find_by_id.assert_not_called()
    request_repository.create.assert_not_called()


def test_create_request_should_raise_error_when_target_level_is_not_greater(
        request_service,
        request_repository,
        employee_repository,
        skill_repository):

    with pytest.raises(
            ValueError,
            match="Target level must be greater than start level"):
        request_service.create_request(4, 2, 1, 1)

    employee_repository.find_by_id.assert_not_called()
    skill_repository.find_by_id.assert_not_called()
    request_repository.create.assert_not_called()


def test_create_request_should_raise_error_when_employee_not_found(
        request_service,
        request_repository,
        employee_repository,
        skill_repository,
        fake_connection):

    employee_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Employee does not exist"):
        request_service.create_request(2, 4, 999, 1)

    employee_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    skill_repository.find_by_id.assert_not_called()
    request_repository.create.assert_not_called()


def test_create_request_should_raise_error_when_skill_not_found(
        request_service,
        request_repository,
        employee_repository,
        skill_repository,
        employee,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    skill_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Skill does not exist"):
        request_service.create_request(2, 4, 1, 999)

    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    skill_repository.find_by_id.assert_called_once_with(999, fake_connection)
    request_repository.create.assert_not_called()


def test_update_request_should_update_when_valid(
        request_service,
        request_repository,
        employee_repository,
        skill_repository,
        employee,
        skill,
        mentorship_request,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    skill_repository.find_by_id.return_value = skill
    request_repository.update.return_value = mentorship_request

    result = request_service.update_request(1, 2, 4, 1, 1)

    assert result == mentorship_request
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    skill_repository.find_by_id.assert_called_once_with(1, fake_connection)
    request_repository.update.assert_called_once_with(
        1,
        2,
        4,
        1,
        1,
        fake_connection
    )


def test_update_request_should_raise_error_when_level_is_invalid(
        request_service,
        request_repository,
        employee_repository,
        skill_repository):

    with pytest.raises(ValueError, match="Level must be between 1 and 5"):
        request_service.update_request(1, 2, 6, 1, 1)

    employee_repository.find_by_id.assert_not_called()
    skill_repository.find_by_id.assert_not_called()
    request_repository.update.assert_not_called()


def test_delete_request_should_return_true_when_deleted(
        request_service,
        request_repository):

    request_repository.delete.return_value = True

    result = request_service.delete_request(1)

    assert result is True
    request_repository.delete.assert_called_once_with(1)


def test_delete_request_should_return_false_when_not_deleted(
        request_service,
        request_repository):

    request_repository.delete.return_value = False

    result = request_service.delete_request(999)

    assert result is False
    request_repository.delete.assert_called_once_with(999)
