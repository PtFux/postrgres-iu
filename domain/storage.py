import logging

from common.contribution_status import ContributionStatus


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
