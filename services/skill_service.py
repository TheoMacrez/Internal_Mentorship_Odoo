from repositories.skill_repository import SkillRepository

class SkillService:

    def __init__(self, skill_repository):
        self.skill_repository = skill_repository

    def get_skill_by_id(self,skill_id):
        return self.skill_repository.find_by_id(skill_id)

    def create_skill(self,name,skill_type):

        already_existing_skill = self.skill_repository.find_by_name(name)

        if already_existing_skill :
            raise ValueError("Skill already exists")

        return self.skill_repository.create(name,skill_type)
    
    def update_skill(self,name,skill_type,skill_id):

        return self.skill_repository.update(name,skill_type,skill_id)

    def delete_skill(self, skill_id):

        return self.skill_repository.delete(skill_id)