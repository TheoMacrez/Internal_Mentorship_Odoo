from datetime import date
from unittest.mock import Mock
import pytest

from models.employee import Employee
from models.mentor_profile import MentorProfile
from models.mentorship import Mentorship
from models.request import Request
from models.skill import Skill
from services.mentorship_service import MentorshipService


@pytest.fixture
def mentorship_repository():
    return Mock()


@pytest.fixture
def mentor_profile_repository():
    return Mock()


@pytest.fixture
def employee_repository():
    return Mock()


@pytest.fixture
def request_repository():
    return Mock()


@pytest.fixture
def skill_repository():
    return Mock()


@pytest.fixture
def mentorship_service(
        mentorship_repository,
        mentor_profile_repository,
        employee_repository,
        request_repository,
        skill_repository):
    return MentorshipService(
        mentorship_repository,
        mentor_profile_repository,
        employee_repository,
        request_repository,
        skill_repository
    )


@pytest.fixture(autouse=True)
def mock_get_connection(patch_get_connection):
    return patch_get_connection("services.mentorship_service.get_connection")


@pytest.fixture
def mentor_profile():
    return MentorProfile(
        id_mentor_profile=1,
        max_mentees=3,
        employee_id=2
    )


@pytest.fixture
def mentee():
    return Employee(
        id_employee=1,
        first_name="Theo",
        last_name="Macrez",
        email="theo@test.com",
        phone="+33600000000",
        birth_date="1995-03-04"
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


@pytest.fixture
def skill():
    return Skill(
        id_skill=1,
        name="PostgreSQL",
        skill_type="TECHNICAL"
    )


@pytest.fixture
def mentorship():
    return Mentorship(
        id_mentorship=1,
        start_date=date(2026, 7, 1),
        end_date=None,
        status="ACCEPTED",
        score=None,
        mentor_profile_id=1,
        mentee_id=1,
        request_id=1,
        skill_id=1
    )


def test_get_all_mentorships_should_return_mentorships(
        mentorship_service,
        mentorship_repository,
        mentorship):

    mentorship_repository.find_all.return_value = [mentorship]

    result = mentorship_service.get_all_mentorships()

    assert result == [mentorship]
    mentorship_repository.find_all.assert_called_once_with()


def test_get_mentorship_by_id_should_return_mentorship(
        mentorship_service,
        mentorship_repository,
        mentorship):

    mentorship_repository.find_by_id.return_value = mentorship

    result = mentorship_service.get_mentorship_by_id(1)

    assert result == mentorship
    mentorship_repository.find_by_id.assert_called_once_with(1)


def test_get_mentorship_by_id_should_return_none_when_not_found(
        mentorship_service,
        mentorship_repository):

    mentorship_repository.find_by_id.return_value = None

    result = mentorship_service.get_mentorship_by_id(999)

    assert result is None
    mentorship_repository.find_by_id.assert_called_once_with(999)


def test_get_mentorships_by_mentor_profile_id_should_return_mentorships(
        mentorship_service,
        mentorship_repository,
        mentor_profile_repository,
        mentor_profile,
        mentorship,
        fake_connection):

    mentor_profile_repository.find_by_id.return_value = mentor_profile
    mentorship_repository.find_by_mentor_profile_id.return_value = [mentorship]

    result = mentorship_service.get_mentorships_by_mentor_profile_id(1)

    assert result == [mentorship]
    mentor_profile_repository.find_by_id.assert_called_once_with(
        1,
        fake_connection
    )
    mentorship_repository.find_by_mentor_profile_id.assert_called_once_with(
        1,
        fake_connection
    )


def test_get_mentorships_by_mentor_profile_id_should_raise_error_when_mentor_profile_not_found(
        mentorship_service,
        mentorship_repository,
        mentor_profile_repository,
        fake_connection):

    mentor_profile_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Mentor profile does not exist"):
        mentorship_service.get_mentorships_by_mentor_profile_id(999)

    mentor_profile_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    mentorship_repository.find_by_mentor_profile_id.assert_not_called()


def test_get_mentorships_by_mentee_id_should_return_mentorships(
        mentorship_service,
        mentorship_repository,
        employee_repository,
        mentee,
        mentorship,
        fake_connection):

    employee_repository.find_by_id.return_value = mentee
    mentorship_repository.find_by_mentee_id.return_value = [mentorship]

    result = mentorship_service.get_mentorships_by_mentee_id(1)

    assert result == [mentorship]
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    mentorship_repository.find_by_mentee_id.assert_called_once_with(
        1,
        fake_connection
    )


def test_get_mentorships_by_mentee_id_should_raise_error_when_mentee_not_found(
        mentorship_service,
        mentorship_repository,
        employee_repository,
        fake_connection):

    employee_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Mentee does not exist"):
        mentorship_service.get_mentorships_by_mentee_id(999)

    employee_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    mentorship_repository.find_by_mentee_id.assert_not_called()


def test_get_mentorship_by_request_id_should_return_mentorship(
        mentorship_service,
        mentorship_repository,
        request_repository,
        mentorship_request,
        mentorship,
        fake_connection):

    request_repository.find_by_id.return_value = mentorship_request
    mentorship_repository.find_by_request_id.return_value = mentorship

    result = mentorship_service.get_mentorship_by_request_id(1)

    assert result == mentorship
    request_repository.find_by_id.assert_called_once_with(1, fake_connection)
    mentorship_repository.find_by_request_id.assert_called_once_with(
        1,
        fake_connection
    )


def test_get_mentorship_by_request_id_should_raise_error_when_request_not_found(
        mentorship_service,
        mentorship_repository,
        request_repository,
        fake_connection):

    request_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Request does not exist"):
        mentorship_service.get_mentorship_by_request_id(999)

    request_repository.find_by_id.assert_called_once_with(999, fake_connection)
    mentorship_repository.find_by_request_id.assert_not_called()


def test_get_mentorships_by_skill_id_should_return_mentorships(
        mentorship_service,
        mentorship_repository,
        skill_repository,
        skill,
        mentorship,
        fake_connection):

    skill_repository.find_by_id.return_value = skill
    mentorship_repository.find_by_skill_id.return_value = [mentorship]

    result = mentorship_service.get_mentorships_by_skill_id(1)

    assert result == [mentorship]
    skill_repository.find_by_id.assert_called_once_with(1, fake_connection)
    mentorship_repository.find_by_skill_id.assert_called_once_with(
        1,
        fake_connection
    )


def test_get_mentorships_by_skill_id_should_raise_error_when_skill_not_found(
        mentorship_service,
        mentorship_repository,
        skill_repository,
        fake_connection):

    skill_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Skill does not exist"):
        mentorship_service.get_mentorships_by_skill_id(999)

    skill_repository.find_by_id.assert_called_once_with(999, fake_connection)
    mentorship_repository.find_by_skill_id.assert_not_called()


def test_get_mentorships_by_status_should_return_mentorships(
        mentorship_service,
        mentorship_repository,
        mentorship):

    mentorship_repository.find_by_status.return_value = [mentorship]

    result = mentorship_service.get_mentorships_by_status("ACCEPTED")

    assert result == [mentorship]
    mentorship_repository.find_by_status.assert_called_once_with("ACCEPTED")


def test_create_mentorship_should_create_when_valid(
        mentorship_service,
        mentorship_repository,
        mentor_profile_repository,
        employee_repository,
        request_repository,
        skill_repository,
        mentor_profile,
        mentee,
        mentorship_request,
        skill,
        mentorship,
        fake_connection):

    mentor_profile_repository.find_by_id.return_value = mentor_profile
    employee_repository.find_by_id.return_value = mentee
    request_repository.find_by_id.return_value = mentorship_request
    skill_repository.find_by_id.return_value = skill
    mentorship_repository.find_by_request_id.return_value = None
    mentorship_repository.create.return_value = mentorship

    result = mentorship_service.create_mentorship(
        date(2026, 7, 1),
        None,
        "ACCEPTED",
        None,
        1,
        1,
        1,
        1
    )

    assert result == mentorship
    mentor_profile_repository.find_by_id.assert_called_once_with(
        1,
        fake_connection
    )
    employee_repository.find_by_id.assert_called_once_with(1, fake_connection)
    request_repository.find_by_id.assert_called_once_with(1, fake_connection)
    skill_repository.find_by_id.assert_called_once_with(1, fake_connection)
    mentorship_repository.find_by_request_id.assert_called_once_with(
        1,
        fake_connection
    )
    mentorship_repository.create.assert_called_once_with(
        date(2026, 7, 1),
        None,
        "ACCEPTED",
        None,
        1,
        1,
        1,
        1,
        fake_connection
    )


def test_create_mentorship_should_raise_error_when_end_date_is_before_start_date(
        mentorship_service,
        mentorship_repository,
        mentor_profile_repository):

    with pytest.raises(
            ValueError,
            match="End date must be after or equal to start date"):
        mentorship_service.create_mentorship(
            date(2026, 7, 10),
            date(2026, 7, 1),
            "ACCEPTED",
            None,
            1,
            1,
            1,
            1
        )

    mentor_profile_repository.find_by_id.assert_not_called()
    mentorship_repository.create.assert_not_called()


def test_create_mentorship_should_raise_error_when_score_is_invalid(
        mentorship_service,
        mentorship_repository,
        mentor_profile_repository):

    with pytest.raises(ValueError, match="Score must be between 1 and 5"):
        mentorship_service.create_mentorship(
            date(2026, 7, 1),
            None,
            "ACCEPTED",
            6,
            1,
            1,
            1,
            1
        )

    mentor_profile_repository.find_by_id.assert_not_called()
    mentorship_repository.create.assert_not_called()


def test_create_mentorship_should_raise_error_when_mentor_profile_not_found(
        mentorship_service,
        mentorship_repository,
        mentor_profile_repository,
        employee_repository,
        fake_connection):

    mentor_profile_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Mentor profile does not exist"):
        mentorship_service.create_mentorship(
            date(2026, 7, 1),
            None,
            "ACCEPTED",
            None,
            999,
            1,
            1,
            1
        )

    mentor_profile_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    employee_repository.find_by_id.assert_not_called()
    mentorship_repository.create.assert_not_called()


def test_create_mentorship_should_raise_error_when_mentee_not_found(
        mentorship_service,
        mentorship_repository,
        mentor_profile_repository,
        employee_repository,
        request_repository,
        mentor_profile,
        fake_connection):

    mentor_profile_repository.find_by_id.return_value = mentor_profile
    employee_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Mentee does not exist"):
        mentorship_service.create_mentorship(
            date(2026, 7, 1),
            None,
            "ACCEPTED",
            None,
            1,
            999,
            1,
            1
        )

    mentor_profile_repository.find_by_id.assert_called_once_with(
        1,
        fake_connection
    )
    employee_repository.find_by_id.assert_called_once_with(
        999,
        fake_connection
    )
    request_repository.find_by_id.assert_not_called()
    mentorship_repository.create.assert_not_called()


def test_create_mentorship_should_raise_error_when_request_not_found(
        mentorship_service,
        mentorship_repository,
        mentor_profile_repository,
        employee_repository,
        request_repository,
        skill_repository,
        mentor_profile,
        mentee,
        fake_connection):

    mentor_profile_repository.find_by_id.return_value = mentor_profile
    employee_repository.find_by_id.return_value = mentee
    request_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Request does not exist"):
        mentorship_service.create_mentorship(
            date(2026, 7, 1),
            None,
            "ACCEPTED",
            None,
            1,
            1,
            999,
            1
        )

    request_repository.find_by_id.assert_called_once_with(999, fake_connection)
    skill_repository.find_by_id.assert_not_called()
    mentorship_repository.create.assert_not_called()


def test_create_mentorship_should_raise_error_when_skill_not_found(
        mentorship_service,
        mentorship_repository,
        mentor_profile_repository,
        employee_repository,
        request_repository,
        skill_repository,
        mentor_profile,
        mentee,
        mentorship_request,
        fake_connection):

    mentor_profile_repository.find_by_id.return_value = mentor_profile
    employee_repository.find_by_id.return_value = mentee
    request_repository.find_by_id.return_value = mentorship_request
    skill_repository.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Skill does not exist"):
        mentorship_service.create_mentorship(
            date(2026, 7, 1),
            None,
            "ACCEPTED",
            None,
            1,
            1,
            1,
            999
        )

    skill_repository.find_by_id.assert_called_once_with(999, fake_connection)
    mentorship_repository.create.assert_not_called()


def test_create_mentorship_should_raise_error_when_request_already_has_mentorship(
        mentorship_service,
        mentorship_repository,
        mentor_profile_repository,
        employee_repository,
        request_repository,
        skill_repository,
        mentor_profile,
        mentee,
        mentorship_request,
        skill,
        mentorship,
        fake_connection):

    mentor_profile_repository.find_by_id.return_value = mentor_profile
    employee_repository.find_by_id.return_value = mentee
    request_repository.find_by_id.return_value = mentorship_request
    skill_repository.find_by_id.return_value = skill
    mentorship_repository.find_by_request_id.return_value = mentorship

    with pytest.raises(
            ValueError,
            match="Mentorship already exists for this request"):
        mentorship_service.create_mentorship(
            date(2026, 7, 1),
            None,
            "ACCEPTED",
            None,
            1,
            1,
            1,
            1
        )

    mentorship_repository.find_by_request_id.assert_called_once_with(
        1,
        fake_connection
    )
    mentorship_repository.create.assert_not_called()


def test_update_mentorship_should_update_when_valid(
        mentorship_service,
        mentorship_repository,
        mentor_profile_repository,
        employee_repository,
        request_repository,
        skill_repository,
        mentor_profile,
        mentee,
        mentorship_request,
        skill,
        mentorship,
        fake_connection):

    mentor_profile_repository.find_by_id.return_value = mentor_profile
    employee_repository.find_by_id.return_value = mentee
    request_repository.find_by_id.return_value = mentorship_request
    skill_repository.find_by_id.return_value = skill
    mentorship_repository.find_by_request_id.return_value = mentorship
    mentorship_repository.update.return_value = mentorship

    result = mentorship_service.update_mentorship(
        1,
        date(2026, 7, 1),
        date(2026, 8, 1),
        "SUCCESS",
        5,
        1,
        1,
        1,
        1
    )

    assert result == mentorship
    mentorship_repository.update.assert_called_once_with(
        1,
        date(2026, 7, 1),
        date(2026, 8, 1),
        "SUCCESS",
        5,
        1,
        1,
        1,
        1,
        fake_connection
    )


def test_update_mentorship_should_raise_error_when_request_has_another_mentorship(
        mentorship_service,
        mentorship_repository,
        mentor_profile_repository,
        employee_repository,
        request_repository,
        skill_repository,
        mentor_profile,
        mentee,
        mentorship_request,
        skill,
        fake_connection):

    other_mentorship = Mentorship(
        id_mentorship=2,
        start_date=date(2026, 7, 1),
        end_date=None,
        status="ACCEPTED",
        score=None,
        mentor_profile_id=1,
        mentee_id=1,
        request_id=1,
        skill_id=1
    )

    mentor_profile_repository.find_by_id.return_value = mentor_profile
    employee_repository.find_by_id.return_value = mentee
    request_repository.find_by_id.return_value = mentorship_request
    skill_repository.find_by_id.return_value = skill
    mentorship_repository.find_by_request_id.return_value = other_mentorship

    with pytest.raises(
            ValueError,
            match="Mentorship already exists for this request"):
        mentorship_service.update_mentorship(
            1,
            date(2026, 7, 1),
            None,
            "ACCEPTED",
            None,
            1,
            1,
            1,
            1
        )

    mentorship_repository.find_by_request_id.assert_called_once_with(
        1,
        fake_connection
    )
    mentorship_repository.update.assert_not_called()


def test_delete_mentorship_should_return_true_when_deleted(
        mentorship_service,
        mentorship_repository):

    mentorship_repository.delete.return_value = True

    result = mentorship_service.delete_mentorship(1)

    assert result is True
    mentorship_repository.delete.assert_called_once_with(1)


def test_delete_mentorship_should_return_false_when_not_deleted(
        mentorship_service,
        mentorship_repository):

    mentorship_repository.delete.return_value = False

    result = mentorship_service.delete_mentorship(999)

    assert result is False
    mentorship_repository.delete.assert_called_once_with(999)
