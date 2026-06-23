from configuration.database_config import get_connection
from repositories.employee_repository import EmployeeRepository
from repositories.mentor_profile_repository import MentorProfileRepository
from repositories.mentorship_repository import MentorshipRepository
from repositories.request_repository import RequestRepository
from repositories.skill_repository import SkillRepository


class MentorshipService:

    def __init__(
            self,
            mentorship_repository,
            mentor_profile_repository,
            employee_repository,
            request_repository,
            skill_repository):
        self.mentorship_repository = mentorship_repository
        self.mentor_profile_repository = mentor_profile_repository
        self.employee_repository = employee_repository
        self.request_repository = request_repository
        self.skill_repository = skill_repository

    def get_all_mentorships(self):
        return self.mentorship_repository.find_all()

    def get_mentorship_by_id(self, id_mentorship):
        return self.mentorship_repository.find_by_id(id_mentorship)

    def get_mentorships_by_mentor_profile_id(self, mentor_profile_id):
        with get_connection() as conn:
            mentor_profile = self.mentor_profile_repository.find_by_id(
                mentor_profile_id,
                conn
            )

            if not mentor_profile:
                raise ValueError("Mentor profile does not exist")

            return self.mentorship_repository.find_by_mentor_profile_id(
                mentor_profile_id,
                conn
            )

    def get_mentorships_by_mentee_id(self, mentee_id):
        with get_connection() as conn:
            mentee = self.employee_repository.find_by_id(mentee_id, conn)

            if not mentee:
                raise ValueError("Mentee does not exist")

            return self.mentorship_repository.find_by_mentee_id(mentee_id, conn)

    def get_mentorship_by_request_id(self, request_id):
        with get_connection() as conn:
            mentorship_request = self.request_repository.find_by_id(
                request_id,
                conn
            )

            if not mentorship_request:
                raise ValueError("Request does not exist")

            return self.mentorship_repository.find_by_request_id(
                request_id,
                conn
            )

    def get_mentorships_by_skill_id(self, skill_id):
        with get_connection() as conn:
            skill = self.skill_repository.find_by_id(skill_id, conn)

            if not skill:
                raise ValueError("Skill does not exist")

            return self.mentorship_repository.find_by_skill_id(skill_id, conn)

    def get_mentorships_by_status(self, status):
        return self.mentorship_repository.find_by_status(status)

    def create_mentorship(
            self,
            start_date,
            end_date,
            status,
            score,
            mentor_profile_id,
            mentee_id,
            request_id,
            skill_id):
        self._validate_dates(start_date, end_date)
        self._validate_score(score)

        with get_connection() as conn:
            self._validate_related_entities(
                mentor_profile_id,
                mentee_id,
                request_id,
                skill_id,
                conn
            )

            existing_mentorship = self.mentorship_repository.find_by_request_id(
                request_id,
                conn
            )

            if existing_mentorship:
                raise ValueError("Mentorship already exists for this request")

            return self.mentorship_repository.create(
                start_date,
                end_date,
                status,
                score,
                mentor_profile_id,
                mentee_id,
                request_id,
                skill_id,
                conn
            )

    def update_mentorship(
            self,
            id_mentorship,
            start_date,
            end_date,
            status,
            score,
            mentor_profile_id,
            mentee_id,
            request_id,
            skill_id):
        self._validate_dates(start_date, end_date)
        self._validate_score(score)

        with get_connection() as conn:
            self._validate_related_entities(
                mentor_profile_id,
                mentee_id,
                request_id,
                skill_id,
                conn
            )

            existing_mentorship = self.mentorship_repository.find_by_request_id(
                request_id,
                conn
            )

            if (
                    existing_mentorship
                    and existing_mentorship.id_mentorship != id_mentorship):
                raise ValueError("Mentorship already exists for this request")

            return self.mentorship_repository.update(
                id_mentorship,
                start_date,
                end_date,
                status,
                score,
                mentor_profile_id,
                mentee_id,
                request_id,
                skill_id,
                conn
            )

    def delete_mentorship(self, id_mentorship):
        return self.mentorship_repository.delete(id_mentorship)

    def _validate_related_entities(
            self,
            mentor_profile_id,
            mentee_id,
            request_id,
            skill_id,
            conn):
        mentor_profile = self.mentor_profile_repository.find_by_id(
            mentor_profile_id,
            conn
        )

        if not mentor_profile:
            raise ValueError("Mentor profile does not exist")

        mentee = self.employee_repository.find_by_id(mentee_id, conn)

        if not mentee:
            raise ValueError("Mentee does not exist")

        mentorship_request = self.request_repository.find_by_id(
            request_id,
            conn
        )

        if not mentorship_request:
            raise ValueError("Request does not exist")

        skill = self.skill_repository.find_by_id(skill_id, conn)

        if not skill:
            raise ValueError("Skill does not exist")

    def _validate_dates(self, start_date, end_date):
        if end_date and end_date < start_date:
            raise ValueError("End date must be after or equal to start date")

    def _validate_score(self, score):
        if score is not None and (score < 1 or score > 5):
            raise ValueError("Score must be between 1 and 5")
