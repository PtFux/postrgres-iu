import logging

from domain.dialogs.dialog_base import DialogBase
from domain.dialogs.dialog_text.user_role_update_text import UserRoleUpdateText
from domain.dialogs.kb.user_role_kb import UserRoleKB
from domain.domain_model.filter import Filter
from domain.domain_model.message_domain import MessageDomain
from domain.domain_model.roles import AllRoles


class UserRoleUpdateDialog(DialogBase):
    filter = Filter.USER_ROLE_UPDATE

    def __init__(self, chat_id, storage, send_message):
        super().__init__(chat_id, storage, send_message)
        self._last_kb = None

    async def start(self, message: MessageDomain):
        logging.info(f"domain: start user role update dialog, text={message.text}")

        if await self._storage.check_registration_by_chat_id(message.chat_id):
            self.temp = self.wait_user_role
            self._last_kb = UserRoleKB()
            builder = self._create_kb_builder(self._last_kb)
            await self._send_message_with_kb(message.chat_id, UserRoleUpdateText.CHOOSE_ROLE, builder.as_markup())
        else:
            await self._send_message(message.chat_id, UserRoleUpdateText.NEED_REGISTRATION)
            return True

    async def wait_user_role(self, message: MessageDomain):
        if message.text in AllRoles().get_role_codes():
            await self._send_message(message.chat_id, UserRoleUpdateText.QUERY_IS_SENDED)
            admin_chat_id = await self._get_admin_chat_id()
            await self._send_message(
                admin_chat_id,
                UserRoleUpdateText.QUERY_FOR_ROLE.format(
                    username=message.username,
                    role=message.text,
                    give_role_cmd=Filter.GIVE_OUT_THE_ROLE,
                    chat_id=message.chat_id)
            )
            return True
        else:
            await self._send_message(message.chat_id, UserRoleUpdateText.NOT_KNOWN)
            builder = self._create_kb_builder(self._last_kb)
            await self._send_message_with_kb(message.chat_id, UserRoleUpdateText.CHOOSE_ROLE, builder.as_markup())

    async def _check_right_student_id(self, student_id):
        return await self._storage.check_right_student_id(student_id)

    async def _get_admin_chat_id(self):
        return await self._storage.get_admin_chat_id()
