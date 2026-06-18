from unittest.mock import Mock
import pytest

from services.skill_service import SkillService
from models.skill import Skill


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def skill_service(mock_repository):
    return SkillService(mock_repository)


@pytest.fixture
def skill():
    return Skill(
        id_skill=1,
        name="PostgreSQL",
        skill_type="TECHNICAL",
    )


def test_get_skill_by_id_should_return_skill(skill_service, mock_repository, skill):
    mock_repository.find_by_id.return_value = skill

    result = skill_service.get_skill_by_id(1)

    assert result == skill
    mock_repository.find_by_id.assert_called_once_with(1)


def test_get_skill_by_id_should_return_none_when_not_found(skill_service, mock_repository):
    mock_repository.find_by_id.return_value = None

    result = skill_service.get_skill_by_id(999)

    assert result is None
    mock_repository.find_by_id.assert_called_once_with(999)


def test_create_skill_should_create_skill_when_name_is_unique(skill_service, mock_repository, skill):
    mock_repository.find_by_name.return_value = None
    mock_repository.create.return_value = skill

    result = skill_service.create_skill("PostgreSQL", "TECHNICAL")

    assert result == skill
    mock_repository.find_by_name.assert_called_once_with("PostgreSQL")
    mock_repository.create.assert_called_once_with("PostgreSQL", "TECHNICAL")


def test_create_skill_should_raise_error_when_name_already_exists(skill_service, mock_repository, skill):
    mock_repository.find_by_name.return_value = skill

    with pytest.raises(ValueError, match="Skill already exists"):
        skill_service.create_skill("PostgreSQL", "TECHNICAL")

    mock_repository.find_by_name.assert_called_once_with("PostgreSQL")
    mock_repository.create.assert_not_called()


def test_update_skill_should_call_repository(skill_service, mock_repository, skill):
    mock_repository.update.return_value = skill

    result = skill_service.update_skill("PostgreSQL", "TECHNICAL", 1)

    assert result == skill
    mock_repository.update.assert_called_once_with("PostgreSQL", "TECHNICAL", 1)


def test_delete_skill_should_return_true_when_deleted(skill_service, mock_repository):
    mock_repository.delete.return_value = True

    result = skill_service.delete_skill(1)

    assert result is True
    mock_repository.delete.assert_called_once_with(1)


def test_delete_skill_should_return_false_when_not_deleted(skill_service, mock_repository):
    mock_repository.delete.return_value = False

    result = skill_service.delete_skill(999)

    assert result is False
    mock_repository.delete.assert_called_once_with(999)