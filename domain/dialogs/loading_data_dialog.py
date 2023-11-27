import logging
import re

from bot.content_type import ContentType
from common.format_contribution_file import FormatContributionFile
from common.user_role_code import UserRoleCode
from domain.cvs_worker import CSVWorker
from domain.dialogs.dialog_base import DialogBase
from domain.dialogs.dialog_text.check_contribution_text import CheckContributionText
from domain.dialogs.dialog_text.loading_data_text import LoadingDataText
from domain.dialogs.dialog_text.user_role_update_text import UserRoleUpdateText
from domain.dialogs.kb.user_role_kb import UserRoleKB, UserRole
from domain.domain_model.filter import Filter
from domain.domain_model.message_domain import MessageDomain


class LoadingDataDialog(DialogBase):
    filter = Filter.LOADING_DATA

    def __init__(self, chat_id, storage, send_message):
        super().__init__(chat_id, storage, send_message)
        self._last_kb = None
        self._enable_role = [UserRoleCode.DUTY, UserRoleCode.ADMIN, UserRoleCode.MODERATOR, UserRoleCode.GOD]

    async def start(self, message: MessageDomain):
        logging.info(f"domain: start loading data dialog, text={message.text}")
        if not await self._storage.check_registration_by_chat_id(message.chat_id):
            await self._send_message(message.chat_id, LoadingDataText.NEED_REGISTRATION)
            return True

        role = await self._storage.get_user_role_from_chat_id(message.chat_id)
        if role in self._enable_role:
            await self._send_message(
                message.chat_id,
                LoadingDataText.WRITE_CSV.format(table=" | ".join(FormatContributionFile().get_headliner()))
            )
            self.temp = self.wait_document_file
        else:
            await self._send_message(
                message.chat_id,
                LoadingDataText.PERMISSION_DENIED
            )
            return True

    async def wait_document_file(self, message: MessageDomain):
        if message.content_type != ContentType.DOCUMENT:
            self._send_message(message.chat_id, LoadingDataText.WAIT_CSV.format(
                table=" | ".join(FormatContributionFile().get_headliner()),
                main_cmd=Filter.MAIN_MENU
            ))
            return True
        try:
            worker = CSVWorker()
            contributions, students = worker.get_contributions_and_students_from_file(message.file_path)
            await self._storage.insert_students(students)
            await self._storage.insert_contributions(contributions)
            await self._send_message(message.chat_id, LoadingDataText.SUCCESSFUL)
        except Exception as e:
            await self._send_message(message.chat_id, LoadingDataText.EXCEPTION)
        return True

