from aiogram.utils.keyboard import InlineKeyboardBuilder

from domain.dialogs.kb.base_kb import BaseKB
from domain.domain_model.message_domain import MessageDomain
from domain.storage import Storage


class DialogBase:
    def __init__(self, chat_id: str | int, storage: Storage, send_message):
        self._chat_id = chat_id
        self.temp = self.start

        self._storage = storage
        self._send_message = send_message

    def start(self, message: MessageDomain):
        pass

    @staticmethod
    def _create_kb_builder(kb: BaseKB):
        builder = InlineKeyboardBuilder()

        for button in kb.buttons.values():
            builder.button(text=button.text, callback_data=button.reply_text)
        builder.adjust(*kb.size)
        return builder

    async def _send_message_with_kb(self, chat_id: str, text: str, builder_kb=None):
        await self._send_message(
            chat_id,
            text,
            markup=builder_kb
        )

    async def _check_right_student_id(self, student_id):
        return await self._storage.check_right_student_id(student_id)

    async def _get_user_role_by_chat_id(self, chat_id: str, default=None):
        return await self._storage.get_user_role_by_chat_id(chat_id, default)


