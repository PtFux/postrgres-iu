import logging
import re

from domain.dialogs.dialog_base import DialogBase
from domain.domain_model.filter import Filter
from domain.domain_model.message_domain import MessageDomain
from domain.dialogs.kb.start_registration_student_id_kb import StartRegistrationStudentIdKB, StatusStudent
from domain.dialogs.dialog_text.registration_text import RegistrationText


class RegistrationDialog(DialogBase):
    filter = Filter.COMMAND_START

    def __init__(self, chat_id, storage, send_message):
        super().__init__(chat_id, storage, send_message)
        self._last_kb = None

    async def start(self, message: MessageDomain):
        logging.info(f"INFO: start registration dialog, text={message.text}")
        await self._send_message_with_kb(message.chat_id, RegistrationText.HELLO)

        self._last_kb = StartRegistrationStudentIdKB()
        builder = self._create_kb_builder(self._last_kb)
        await self._send_message_with_kb(message.chat_id, RegistrationText.NEED_REGISTRATION, builder.as_markup())

        self.temp = self.get_status_student_or_no_student

    async def get_status_student_or_no_student(self, message: MessageDomain):
        if message.text == self._last_kb.buttons.get(StatusStudent.STUDENT).reply_text or \
                message.reply_text == self._last_kb.buttons.get(StatusStudent.STUDENT).reply_text:
            self.temp = self.wait_student_id
            await self._send_message_with_kb(message.chat_id, RegistrationText.NEED_STUDENT_ID)
        elif message.text == self._last_kb.buttons.get(StatusStudent.NO_STUDENT).reply_text or \
                message.reply_text == self._last_kb.buttons.get(StatusStudent.NO_STUDENT).reply_text:
            await self._send_message_with_kb(message.chat_id, RegistrationText.NO_STUDENT)
        else:
            await self._send_message_with_kb(message.chat_id, RegistrationText.NO_KNOWN)
            builder = self._create_kb_builder(self._last_kb)
            await self._send_message_with_kb(message.chat_id, RegistrationText.NEED_REGISTRATION, builder.as_markup())

    async def wait_student_id(self, message: MessageDomain):
        self.temp = self.get_status_student_or_no_student
        if await self._check_right_student_id(message.text):
            if await self._check_registration(message.chat_id):
                await self._send_message_with_kb(message.chat_id, RegistrationText.AGAIN_REGISTRATION)
                return True
            else:
                if await self._storage.add_default_user(message.chat_id):
                    await self._send_message_with_kb(message.chat_id, RegistrationText.SUCCESSFUL_REGISTRATION)
                    return True
                else:
                    await self._send_message_with_kb(message.chat_id, RegistrationText.NOT_SUCCESSFUL_REGISTRATION)
        else:
            await self._send_message_with_kb(message.chat_id, RegistrationText.NEED_REGISTRATION)

    async def _check_right_student_id(self, student_id):
        return re.fullmatch(r'\d\d\w\d\d\d\d', student_id)

    async def _check_registration(self, chat_id):
        return await self._storage.check_registration_by_chat_id(chat_id)
