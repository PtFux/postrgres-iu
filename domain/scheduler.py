import logging

from domain.dialogs.check_contribution_dialog import CheckContributionDialog
from domain.dialogs.dialog_base import DialogBase
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
        print(self.dialogs)
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
            case _:
                if message.chat_id in self.dialogs:
                    dialog = self.dialogs.get(message.chat_id)
                else:
                    if message.text == "/start":
                        dialog = RegistrationDialog(message.chat_id, self._storage, send_message=self._send_message)
                        self.dialogs.update({message.chat_id: dialog})
                    else:
                        dialog = RegistrationDialog(message.chat_id, self._storage, self._send_message)
        print(self.dialogs)
        print(dialog.temp)
        end = await dialog.temp(message)
        if end:
            self.dialogs.pop(message.chat_id)
            logging.info(f"Scheduler: Finished dialog for user id={message.chat_id} dialogs={self.dialogs}")
