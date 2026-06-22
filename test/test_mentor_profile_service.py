from unittest.mock import Mock
import pytest

from models.employee import Employee
from models.mentor_profile import MentorProfile
from services.mentor_profile_service import MentorProfileService


@pytest.fixture
def mentor_profile_repository():
    return Mock()


@pytest.fixture
def employee_repository():
    return Mock()


@pytest.fixture
def mentor_profile_service(mentor_profile_repository, employee_repository):
    return MentorProfileService(
        mentor_profile_repository,
        employee_repository
    )


@pytest.fixture(autouse=True)
def mock_get_connection(patch_get_connection):
    return patch_get_connection("services.mentor_profile_service.get_connection")


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
def mentor_profile():
    return MentorProfile(
        id_mentor_profile=1,
        max_mentees=3,
        employee_id=1
    )


def test_get_all_mentor_profiles_should_return_mentor_profiles(
        mentor_profile_service,
        mentor_profile_repository,
        mentor_profile):

    mentor_profile_repository.find_all.return_value = [mentor_profile]

    result = mentor_profile_service.get_all_mentor_profiles()

    assert result == [mentor_profile]
    mentor_profile_repository.find_all.assert_called_once_with()


def test_get_mentor_profile_by_id_should_return_mentor_profile(
        mentor_profile_service,
        mentor_profile_repository,
        mentor_profile):

    mentor_profile_repository.find_by_id.return_value = mentor_profile

    result = mentor_profile_service.get_mentor_profile_by_id(1)

    assert result == mentor_profile
    mentor_profile_repository.find_by_id.assert_called_once_with(1)


def test_get_mentor_profile_by_id_should_return_none_when_not_found(
        mentor_profile_service,
        mentor_profile_repository):

    mentor_profile_repository.find_by_id.return_value = None

    result = mentor_profile_service.get_mentor_profile_by_id(999)

    assert result is None
    mentor_profile_repository.find_by_id.assert_called_once_with(999)


def test_get_mentor_profile_by_employee_id_should_return_mentor_profile(
        mentor_profile_service,
        mentor_profile_repository,
        employee_repository,
        employee,
        mentor_profile,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    mentor_profile_repository.find_by_employee_id.return_value = mentor_profile

    result = mentor_profile_service.get_mentor_profile_by_employee_id(1)

    assert result == mentor_profile
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    mentor_profile_repository.find_by_employee_id.assert_called_once_with(
        1,
        fake_connection
    )


def test_get_mentor_profile_by_employee_id_should_raise_error_when_employee_not_found(
        mentor_profile_service,
        mentor_profile_repository,
        employee_repository,
        fake_connection):

    employee_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Employee does not exist"):
        mentor_profile_service.get_mentor_profile_by_employee_id(999)

    employee_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    mentor_profile_repository.find_by_employee_id.assert_not_called()


def test_create_mentor_profile_should_create_when_valid(
        mentor_profile_service,
        mentor_profile_repository,
        employee_repository,
        employee,
        mentor_profile,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    mentor_profile_repository.find_by_employee_id.return_value = None
    mentor_profile_repository.create.return_value = mentor_profile

    result = mentor_profile_service.create_mentor_profile(3, 1)

    assert result == mentor_profile
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    mentor_profile_repository.find_by_employee_id.assert_called_once_with(
        1,
        fake_connection
    )
    mentor_profile_repository.create.assert_called_once_with(
        3,
        1,
        fake_connection
    )


def test_create_mentor_profile_should_raise_error_when_max_mentees_is_invalid(
        mentor_profile_service,
        mentor_profile_repository,
        employee_repository):

    with pytest.raises(ValueError, match="Max mentees must be greater than 0"):
        mentor_profile_service.create_mentor_profile(0, 1)

    employee_repository.find_by_id.assert_not_called()
    mentor_profile_repository.create.assert_not_called()


def test_create_mentor_profile_should_raise_error_when_employee_not_found(
        mentor_profile_service,
        mentor_profile_repository,
        employee_repository,
        fake_connection):

    employee_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Employee does not exist"):
        mentor_profile_service.create_mentor_profile(3, 999)

    employee_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    mentor_profile_repository.find_by_employee_id.assert_not_called()
    mentor_profile_repository.create.assert_not_called()


def test_create_mentor_profile_should_raise_error_when_profile_already_exists(
        mentor_profile_service,
        mentor_profile_repository,
        employee_repository,
        employee,
        mentor_profile,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    mentor_profile_repository.find_by_employee_id.return_value = mentor_profile

    with pytest.raises(
            ValueError,
            match="Mentor profile already exists for this employee"):
        mentor_profile_service.create_mentor_profile(3, 1)

    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    mentor_profile_repository.find_by_employee_id.assert_called_once_with(
        1,
        fake_connection
    )
    mentor_profile_repository.create.assert_not_called()


def test_update_mentor_profile_should_update_when_valid(
        mentor_profile_service,
        mentor_profile_repository,
        employee_repository,
        employee,
        mentor_profile,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    mentor_profile_repository.find_by_employee_id.return_value = mentor_profile
    mentor_profile_repository.update.return_value = mentor_profile

    result = mentor_profile_service.update_mentor_profile(1, 3, 1)

    assert result == mentor_profile
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    mentor_profile_repository.find_by_employee_id.assert_called_once_with(
        1,
        fake_connection
    )
    mentor_profile_repository.update.assert_called_once_with(
        1,
        3,
        1,
        fake_connection
    )


def test_update_mentor_profile_should_raise_error_when_max_mentees_is_invalid(
        mentor_profile_service,
        mentor_profile_repository,
        employee_repository):

    with pytest.raises(ValueError, match="Max mentees must be greater than 0"):
        mentor_profile_service.update_mentor_profile(1, 0, 1)

    employee_repository.find_by_id.assert_not_called()
    mentor_profile_repository.update.assert_not_called()


def test_update_mentor_profile_should_raise_error_when_employee_not_found(
        mentor_profile_service,
        mentor_profile_repository,
        employee_repository,
        fake_connection):

    employee_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Employee does not exist"):
        mentor_profile_service.update_mentor_profile(1, 3, 999)

    employee_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    mentor_profile_repository.find_by_employee_id.assert_not_called()
    mentor_profile_repository.update.assert_not_called()


def test_update_mentor_profile_should_raise_error_when_employee_has_another_profile(
        mentor_profile_service,
        mentor_profile_repository,
        employee_repository,
        employee,
        fake_connection):

    other_mentor_profile = MentorProfile(
        id_mentor_profile=2,
        max_mentees=3,
        employee_id=1
    )

    employee_repository.find_by_id.return_value = employee
    mentor_profile_repository.find_by_employee_id.return_value = other_mentor_profile

    with pytest.raises(
            ValueError,
            match="Mentor profile already exists for this employee"):
        mentor_profile_service.update_mentor_profile(1, 3, 1)

    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    mentor_profile_repository.find_by_employee_id.assert_called_once_with(
        1,
        fake_connection
    )
    mentor_profile_repository.update.assert_not_called()


def test_delete_mentor_profile_should_return_true_when_deleted(
        mentor_profile_service,
        mentor_profile_repository):

    mentor_profile_repository.delete.return_value = True

    result = mentor_profile_service.delete_mentor_profile(1)

    assert result is True
    mentor_profile_repository.delete.assert_called_once_with(1)


def test_delete_mentor_profile_should_return_false_when_not_deleted(
        mentor_profile_service,
        mentor_profile_repository):

    mentor_profile_repository.delete.return_value = False

    result = mentor_profile_service.delete_mentor_profile(999)

    assert result is False
    mentor_profile_repository.delete.assert_called_once_with(999)
