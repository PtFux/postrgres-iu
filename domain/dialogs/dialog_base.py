from domain.domain_model.message_domain import MessageDomain
from domain.storage import Storage


class DialogBase:
    def __init__(self, chat_id: str | int, storage: Storage):
        self._chat_id = chat_id
        self.temp = self.start

        self._storage = storage

    def start(self, message: MessageDomain):
        pass
