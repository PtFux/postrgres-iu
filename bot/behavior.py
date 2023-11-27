import logging
import pathlib

from aiogram import Bot, Dispatcher, Router, types
from aiogram import F

from bot.content_type import ContentType
from common.format_contribution_file import FormatContributionFile
from domain.domain_model.message_domain import MessageDomain
from domain.scheduler import Scheduler


class Behavior:

    def __init__(self, dp: Dispatcher, bot: Bot):
        self._dp = dp
        self._bot = bot
        self._scheduler = Scheduler(self.send_message)

    def configure(self):
        logging.info(f"bot: Configure behavior")
        router_test = Router(name="test")

        router_test.message.register(self.document_message_handler, F.content_type == "document")
        router_test.message.register(self.message_handler)

        router_test.callback_query.register(self.callback_query_handler)

        self._dp.include_router(router_test)

    async def callback_query_handler(self, callback_query: types.CallbackQuery):
        logging.info(f"bot: Received callback_query from id={callback_query.message.chat.id} data={callback_query.data}")

        await self._scheduler.handle_message(MessageDomain(
            str(callback_query.message.chat.id),
            callback_query.data,
            username=callback_query.message.chat.username,
            content_type=ContentType.TEXT
        ))

    async def message_handler(self, message: types.Message) -> None:
        logging.info(f"bot: Received message from user id={message.chat.id} with text={message.text}")
        print(message.document)

        await self._scheduler.handle_message(MessageDomain(
            str(message.chat.id),
            message.text,
            username=message.chat.username,
            content_type=ContentType.TEXT
        ))

    async def document_message_handler(self, message: types.Message):
        logging.info(f"Received document from user={message.chat.username} \
        id={message.chat.id} with document={message.document.file_name}")

        file_path = await self.download_file(message.document)
        await self._scheduler.handle_message(MessageDomain(
            str(message.chat.id),
            message.text,
            username=message.chat.username,
            content_type=ContentType.DOCUMENT,
            file_path=file_path
        ))

    async def download_file(self, document: types.Document) -> pathlib.Path:
        file = await self._bot.get_file(document.file_id)
        file_path = file.file_path
        local_file_path = FormatContributionFile.path

        logging.info(f"bot: Downloading file {document.file_name} in {local_file_path}")
        await self._bot.download_file(file_path, local_file_path)
        return local_file_path

    async def send_message(self,
                           chat_id: str,
                           text: str,
                           markup=None):
        await self._bot.send_message(chat_id, text, reply_markup=markup)
