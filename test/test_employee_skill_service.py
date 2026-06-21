from unittest.mock import Mock
import pytest

from services.employee_skill_service import EmployeeSkillService
from models.employee import Employee
from models.skill import Skill
from models.employee_skill import EmployeeSkill


@pytest.fixture
def employee_skill_repository():
    return Mock()


@pytest.fixture
def employee_repository():
    return Mock()


@pytest.fixture
def skill_repository():
    return Mock()


@pytest.fixture
def employee_skill_service(
        employee_skill_repository,
        employee_repository,
        skill_repository):
    return EmployeeSkillService(
        employee_skill_repository,
        employee_repository,
        skill_repository
    )


@pytest.fixture(autouse=True)
def mock_get_connection(patch_get_connection):
    return patch_get_connection("services.employee_skill_service.get_connection")


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
def employee_skill():
    return EmployeeSkill(
        level=3,
        employee_id=1,
        skill_id=1
    )


def test_get_skills_by_employee_id_should_return_employee_skills(
        employee_skill_service,
        employee_skill_repository,
        employee_repository,
        employee,
        employee_skill,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    employee_skill_repository.find_by_employee_id.return_value = [employee_skill]

    result = employee_skill_service.get_skills_by_employee_id(1)

    assert result == [employee_skill]
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    employee_skill_repository.find_by_employee_id.assert_called_once_with(
        1,
        fake_connection
    )


def test_get_skills_by_employee_id_should_raise_error_when_employee_not_found(
        employee_skill_service,
        employee_repository,
        employee_skill_repository,
        fake_connection):

    employee_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Employee does not exist"):
        employee_skill_service.get_skills_by_employee_id(999)

    employee_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    employee_skill_repository.find_by_employee_id.assert_not_called()


def test_get_employees_by_skill_id_should_return_employee_skills(
        employee_skill_service,
        employee_skill_repository,
        skill_repository,
        skill,
        employee_skill,
        fake_connection):

    skill_repository.find_by_id.return_value = skill
    employee_skill_repository.find_by_skill_id.return_value = [employee_skill]

    result = employee_skill_service.get_employees_by_skill_id(1)

    assert result == [employee_skill]
    skill_repository.find_by_id.assert_called_once_with(1, fake_connection)
    employee_skill_repository.find_by_skill_id.assert_called_once_with(
        1,
        fake_connection
    )


def test_get_employees_by_skill_id_should_raise_error_when_skill_not_found(
        employee_skill_service,
        skill_repository,
        employee_skill_repository,
        fake_connection):

    skill_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Skill does not exist"):
        employee_skill_service.get_employees_by_skill_id(999)

    skill_repository.find_by_id.assert_called_once_with(999, fake_connection)
    employee_skill_repository.find_by_skill_id.assert_not_called()


def test_assign_skill_to_employee_should_assign_when_valid(
        employee_skill_service,
        employee_skill_repository,
        employee_repository,
        skill_repository,
        employee,
        skill,
        employee_skill,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    skill_repository.find_by_id.return_value = skill
    employee_skill_repository.find_by_employee_id.return_value = []
    employee_skill_repository.assign_employee_skill.return_value = employee_skill

    result = employee_skill_service.assign_skill_to_employee(1, 1, 3)

    assert result == employee_skill

    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    skill_repository.find_by_id.assert_called_once_with(1, fake_connection)
    employee_skill_repository.find_by_employee_id.assert_called_once_with(
        1,
        fake_connection
    )
    employee_skill_repository.assign_employee_skill.assert_called_once_with(
        3,
        1,
        1,
        fake_connection
    )


def test_assign_skill_to_employee_should_raise_error_when_employee_not_found(
        employee_skill_service,
        employee_repository,
        skill_repository,
        employee_skill_repository,
        fake_connection):

    employee_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Employee does not exist"):
        employee_skill_service.assign_skill_to_employee(999, 1, 3)

    employee_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    skill_repository.find_by_id.assert_not_called()
    employee_skill_repository.assign_employee_skill.assert_not_called()


def test_assign_skill_to_employee_should_raise_error_when_skill_not_found(
        employee_skill_service,
        employee_repository,
        skill_repository,
        employee_skill_repository,
        employee,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    skill_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Skill does not exist"):
        employee_skill_service.assign_skill_to_employee(1, 999, 3)

    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    skill_repository.find_by_id.assert_called_once_with(999, fake_connection)
    employee_skill_repository.assign_employee_skill.assert_not_called()


def test_assign_skill_to_employee_should_raise_error_when_level_is_invalid(
        employee_skill_service,
        employee_repository,
        skill_repository,
        employee_skill_repository,
        employee,
        skill):

    employee_repository.find_by_id.return_value = employee
    skill_repository.find_by_id.return_value = skill

    with pytest.raises(ValueError, match="Level must be between 1 and 5"):
        employee_skill_service.assign_skill_to_employee(1, 1, 6)

    employee_repository.find_by_id.assert_not_called()
    skill_repository.find_by_id.assert_not_called()
    employee_skill_repository.assign_employee_skill.assert_not_called()


def test_assign_skill_to_employee_should_raise_error_when_skill_already_assigned(
        employee_skill_service,
        employee_repository,
        skill_repository,
        employee_skill_repository,
        employee,
        skill,
        employee_skill,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    skill_repository.find_by_id.return_value = skill
    employee_skill_repository.find_by_employee_id.return_value = [employee_skill]

    with pytest.raises(ValueError, match="Skill already assigned to employee"):
        employee_skill_service.assign_skill_to_employee(1, 1, 3)

    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    skill_repository.find_by_id.assert_called_once_with(1, fake_connection)
    employee_skill_repository.find_by_employee_id.assert_called_once_with(
        1,
        fake_connection
    )
    employee_skill_repository.assign_employee_skill.assert_not_called()


def test_update_employee_skill_level_should_update_when_valid(
        employee_skill_service,
        employee_skill_repository,
        employee_repository,
        skill_repository,
        employee,
        skill,
        employee_skill,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    skill_repository.find_by_id.return_value = skill
    employee_skill_repository.update_skill_level.return_value = employee_skill

    result = employee_skill_service.update_employee_skill_level(1, 1, 3)

    assert result == employee_skill
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    skill_repository.find_by_id.assert_called_once_with(1, fake_connection)
    employee_skill_repository.update_skill_level.assert_called_once_with(
        3,
        1,
        1,
        fake_connection
    )


def test_update_employee_skill_level_should_raise_error_when_level_is_invalid(
        employee_skill_service,
        employee_repository,
        skill_repository,
        employee_skill_repository):

    with pytest.raises(ValueError, match="Level must be between 1 and 5"):
        employee_skill_service.update_employee_skill_level(1, 1, 0)

    employee_repository.find_by_id.assert_not_called()
    skill_repository.find_by_id.assert_not_called()
    employee_skill_repository.update_skill_level.assert_not_called()


def test_remove_skill_from_employee_should_return_true_when_deleted(
        employee_skill_service,
        employee_skill_repository,
        employee_repository,
        skill_repository,
        employee,
        skill,
        fake_connection):

    employee_repository.find_by_id.return_value = employee
    skill_repository.find_by_id.return_value = skill
    employee_skill_repository.delete.return_value = True

    result = employee_skill_service.remove_skill_from_employee(1, 1)

    assert result is True
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    skill_repository.find_by_id.assert_called_once_with(1, fake_connection)
    employee_skill_repository.delete.assert_called_once_with(
        1,
        1,
        fake_connection
    )
