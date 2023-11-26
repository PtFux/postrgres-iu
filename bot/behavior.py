import asyncio
import logging
import sys
import html
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from domain.domain_model.message_domain import MessageDomain
from domain.scheduler import Scheduler


class Behavior:

    def __init__(self, dp: Dispatcher, bot: Bot):
        self._dp = dp
        self._bot = bot
        self._scheduler = Scheduler(self.send_message)

    def configure(self):
        logging.info(f"INFO: Configure behavior")
        router_test = Router(name="test")

        # router_test.message.register(self.command_start_handler, CommandStart())

        router_test.message.register(self.echo_handler)

        router_test.callback_query.register(self.callback_query_handler)

        self._dp.include_router(router_test)

    async def callback_query_handler(self, callback_query: types.CallbackQuery):
        logging.info(f"INFO: Received callback_query from id={callback_query.message.chat.id} data={callback_query.data}")
        await self._scheduler.handle_message(MessageDomain(
            str(callback_query.message.chat.id),
            callback_query.data,
            username=callback_query.message.chat.username
        ))

    # async def command_start_handler(self, message: Message) -> None:
    #     """
    #     This handler receives messages with `/start` command
    #     """
    #     # Most event objects have aliases for API methods that can be called in events' context
    #     # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    #     # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    #     # method automatically or call API method directly via
    #     # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    #     print(message.chat.id, message.text)
    #     await self._scheduler.handle_message(MessageDomain(
    #         str(message.chat.id),
    #         message.text
    #     ))
    #     await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

    async def echo_handler(self, message: types.Message) -> None:
        logging.info(f"Received message from user id={message.chat.id} with text={message.text}")

        await self._scheduler.handle_message(MessageDomain(
            str(message.chat.id),
            message.text,
            username=message.chat.username
        ))

    async def send_message(self,
                           chat_id: str,
                           text: str,
                           markup=None):
        await self._bot.send_message(chat_id, text, reply_markup=markup)

    async def _create_keyboard(self, keyboard_buttons, keyboard_width, save_previous_keyboard):
        return
