import logging

from domain.dialogs.check_contribution_dialog import CheckContributionDialog
from domain.dialogs.dialog_base import DialogBase
from domain.dialogs.dialog_text.main_menu_text import MainMenuText
from domain.dialogs.kb.main_menu_kb import MainMenuKB
from domain.dialogs.loading_data_dialog import LoadingDataDialog
from domain.dialogs.main_ratings_dialog import MainRatingsDialog
from domain.dialogs.registration_dialog import RegistrationDialog
from domain.dialogs.user_role_update_dialog import UserRoleUpdateDialog
from domain.domain_model.filter import Filter
from domain.domain_model.message_domain import MessageDomain
from domain.domain_model.roles import AllRoles

dialogs = [RegistrationDialog, CheckContributionDialog, UserRoleUpdateDialog, LoadingDataDialog, MainRatingsDialog]


class MainMenuDialog(DialogBase):
    filter = Filter.MAIN_MENU
    right = "can_do_with_main_menu"

    def __init__(self, chat_id, storage, send_message):
        super().__init__(chat_id, storage, send_message)
        self._last_kb = None
        self._all_roles = AllRoles()

    async def start(self, message: MessageDomain):
        logging.info(f"domain: start main menu dialog, text={message.text}")

        role = await self._storage.get_user_role_by_chat_id(message.chat_id)
        markup_kb = await self._get_markup_kb_by_role(role)
        await self._send_message_with_kb(message.chat_id, MainMenuText.CHOOSE_DO, markup_kb)
        return True

    async def _get_markup_kb_by_role(self, role_code: str):
        role = self._all_roles.get_role_by_role_code(role_code)

        dialog_buttons = {
            dialog.filter: {"name": dialog.name, "reply_text": dialog.filter} for dialog in dialogs
            if (getattr(role, dialog.right, False) if role else True)
        }
        kb = MainMenuKB(dialog_buttons)
        return self._create_kb_builder(kb).as_markup()
