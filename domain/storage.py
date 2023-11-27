import logging
import re

from common.contribution_status import ContributionStatus
from common.user_role_code import UserRoleCode
from domain.domain_model.contribution import Contribution


class Storage:
    def __init__(self):
        pass

    async def add_default_user(self, chat_id: str):
        logging.info(f"INFO: Storage: Added new default user with chat_id = {chat_id}")
        return True

    async def check_registration_by_chat_id(self, chat_id: str):
        return True

    async def get_status_contribution_by_student_id_number(self, student_id_number: str):
        return ContributionStatus.STUDENTSHIP

    async def get_admin_chat_id(self):
        return "748216079"

    async def get_user_role_from_chat_id(self, chat_id: str):
        return UserRoleCode.DUTY

    async def check_right_student_id(self, student_id_number):
        return re.fullmatch(r'\d\d\w\d\d\d\d', student_id_number)

    async def insert_students(self, students: list[dict]):
        print(*students, sep="\n")

    async def insert_contributions(self, contributions: list[Contribution]):
        print(*contributions, sep="\n")
