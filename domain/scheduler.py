import logging

from bot.content_type import ContentType
from domain.dialogs.check_contribution_dialog import CheckContributionDialog
from domain.dialogs.dialog_base import DialogBase
from domain.dialogs.loading_data_dialog import LoadingDataDialog
from domain.dialogs.main_ratings_dialog import MainRatingsDialog
from domain.dialogs.registration_dialog import RegistrationDialog
from domain.dialogs.user_role_update_dialog import UserRoleUpdateDialog
from domain.domain_model.message_domain import MessageDomain
from domain.storage import Storage


class Scheduler:

    def __init__(self, send_message):
        self.dialogs: dict[str, DialogBase] = {}
        self._send_message = send_message

        self._storage = Storage()

    async def handle_message(self, message: MessageDomain):

        match message.text:
            case RegistrationDialog.filter:
                dialog = RegistrationDialog(message.chat_id, self._storage, send_message=self._send_message)
                self.dialogs.update({message.chat_id: dialog})
            case CheckContributionDialog.filter:
                dialog = CheckContributionDialog(message.chat_id, self._storage, send_message=self._send_message)
                self.dialogs.update({message.chat_id: dialog})
            case UserRoleUpdateDialog.filter:
                dialog = UserRoleUpdateDialog(message.chat_id, self._storage, send_message=self._send_message)
                self.dialogs.update({message.chat_id: dialog})
            case LoadingDataDialog.filter:
                dialog = LoadingDataDialog(message.chat_id, self._storage, send_message=self._send_message)
                self.dialogs.update({message.chat_id: dialog})
            case MainRatingsDialog.filter:
                dialog = MainRatingsDialog(message.chat_id, self._storage, send_message=self._send_message)
                self.dialogs.update({message.chat_id: dialog})
            case _:
                if message.chat_id in self.dialogs:
                    dialog = self.dialogs.get(message.chat_id)
                else:
                    dialog = RegistrationDialog(message.chat_id, self._storage, send_message=self._send_message)
                    self.dialogs.update({message.chat_id: dialog})

        end = await dialog.temp(message)
        if end:
            self.dialogs.pop(message.chat_id)
            logging.info(f"Scheduler: Finished dialog for user id={message.chat_id} dialogs={self.dialogs}")
