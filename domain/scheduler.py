from domain.dialogs.dialog_base import DialogBase
from domain.dialogs.registration_dialog import RegistrationDialog
from domain.domain_model.message_domain import MessageDomain


class Scheduler:

    def __init__(self, send_message):
        self.dialogs: dict[str, DialogBase] = {}
        self._send_message = send_message

    async def handle_message(self, message: MessageDomain):
        if message.chat_id in self.dialogs:
            dialog = self.dialogs.get(message.chat_id)
        else:
            if message.text == "/start":
                dialog = RegistrationDialog(message.chat_id, None, send_message=self._send_message)
                self.dialogs.update({message.chat_id: dialog})
            else:
                dialog = RegistrationDialog(message.chat_id, None, self._send_message)
        await dialog.temp(message)

