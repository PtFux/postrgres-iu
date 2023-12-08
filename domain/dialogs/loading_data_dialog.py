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
from domain.domain_model.roles import AllRoles


class LoadingDataDialog(DialogBase):
    filter = Filter.LOADING_DATA
    right = "can_loading_data"
    name = LoadingDataText.NAME

    def __init__(self, chat_id, storage, send_message):
        super().__init__(chat_id, storage, send_message)
        self._last_kb = None
        self._enable_role = AllRoles().get_enable_role_code_by_atr_name(self.right)

        self._contributions = None
        self._students = None

    async def start(self, message: MessageDomain):
        logging.info(f"domain: start loading data dialog, text={message.text}")

        role = await self._get_user_role_by_chat_id(message.chat_id)
        if not role:
            await self._send_message(message.chat_id, LoadingDataText.NEED_REGISTRATION)
            return True
        elif role in self._enable_role:
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
            self._contributions, self._students = worker.get_contributions_and_students_from_file(message.file_path)
            await self._send_message(message.chat_id,
                                     LoadingDataText.CONFIRM_LOADING.format(code_agree=LoadingDataText.AGREE_LOADING))
            text_table_for_cont = "\n".join(str(cont) for cont in self._contributions)
            text_table_for_student = "\n".join(str(student) for student in self._students)
            await self._send_message(message.chat_id,
                                     LoadingDataText.TABLE_ST_CONT.format(student_table=text_table_for_student,
                                                                          cont_table=text_table_for_cont))
            self.temp = self.get_access_for_loading
        except Exception as e:
            print(e)
            await self._send_message(message.chat_id, LoadingDataText.EXCEPTION)

    async def get_access_for_loading(self, message: MessageDomain):
        if message.text == LoadingDataText.AGREE_LOADING:
            try:
                await self.load_data_contribution_and_students()
                await self._send_message(message.chat_id, LoadingDataText.SUCCESSFUL)
            except Exception as e:
                await self._send_message(message.chat_id, LoadingDataText.EXCEPTION)
            return True
        self.temp = self.start

    async def load_data_contribution_and_students(self):
        no_exist_students = await self._storage.insert_students(self._students)
        await self._storage.insert_default_ratings_for_many_students(no_exist_students)
        await self._storage.insert_contributions(self._contributions)
