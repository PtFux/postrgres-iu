import logging

from domain.dialogs.dialog_base import DialogBase
from domain.dialogs.dialog_text.main_ratings_text import MainRatingsText
from domain.dialogs.dialog_text.user_role_update_text import UserRoleUpdateText
from domain.dialogs.kb.main_ratings_kb import MainRatingsKB
from domain.dialogs.kb.user_role_kb import UserRoleKB
from domain.domain_model.filter import Filter
from domain.domain_model.message_domain import MessageDomain
from domain.domain_model.roles import AllRoles


class MainRatingsDialog(DialogBase):
    filter = Filter.MAIN_RATINGS

    def __init__(self, chat_id, storage, send_message):
        super().__init__(chat_id, storage, send_message)
        self._last_kb = None
        self._all_roles = AllRoles()
        self.rights = {
            "can_give_promo_code": {"name": "Выдать промокод", "func": self.give_promo_code},
            "can_check_other_rating": {"name": "Посмотреть свой", "func": self.check_other_rating},
            "can_check_rating_stat": {"name": "Посмотреть топ", "func": self.check_rating_stat},
            "can_update_rating": {"name": "Изменить рейтинг", "func": self.update_ratings},
            "can_check_self_rating": {"name": "Посмотреть свой рейтинг", "func": self.check_self_rating}
        }

    async def start(self, message: MessageDomain):
        logging.info(f"domain: start main ratings dialog, text={message.text}")

        role = await self._storage.get_user_role_by_chat_id(message.chat_id)
        markup_kb = await self._get_markup_kb_by_role(role)
        await self._send_message_with_kb(message.chat_id, MainRatingsText.CHOOSE_DO, markup_kb)
        self.temp = self.wait_right_for_ratings

    async def wait_right_for_ratings(self, message: MessageDomain):

        role_code = await self._storage.get_user_role_by_chat_id(message.chat_id)
        temp_right = self.rights.get(message.text)
        if not temp_right:
            markup_kb = await self._get_markup_kb_by_role(role_code)
            await self._send_message_with_kb(message.chat_id, MainRatingsText.NO_KNOWN, markup_kb)
            return

        enable_roles = self._all_roles.get_enable_role_code_by_atr_name(message.text)
        if role_code in enable_roles:
            self.temp = temp_right.get("func")
            await self._send_message(message.chat_id,
                                     MainRatingsText.ACCESS_MOVE_TO.format(button_name=temp_right.get("name")))
        else:
            markup_kb = await self._get_markup_kb_by_role(role_code)
            await self._send_message_with_kb(message.chat_id, MainRatingsText.PERMISSION_DENIED, markup_kb)

    async def _get_markup_kb_by_role(self, role_code: str):
        role = self._all_roles.get_role_by_role_code(role_code)
        if not role:
            return
        enable_rights = {
            right: self.rights.get(right) for right in self.rights.keys()
            if getattr(role, right, False)
        }
        kb = MainRatingsKB(enable_rights)
        return self._create_kb_builder(kb).as_markup()

    async def update_ratings(self, message: MessageDomain):
        print(message.text)

    async def give_promo_code(self, message: MessageDomain):
        print(message.text)

    async def check_self_rating(self, message: MessageDomain):
        print(message.text)

    async def check_other_rating(self, message: MessageDomain):
        print(message.text)

    async def check_rating_stat(self, message: MessageDomain):
        print(message.text)
