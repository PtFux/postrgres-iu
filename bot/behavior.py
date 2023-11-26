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
        router_test = Router(name="test")

        router_test.message.register(self.command_start_handler, CommandStart())

        router_test.message.register(self.echo_handler)

        self._dp.include_router(router_test)

    async def command_start_handler(self, message: Message) -> None:
        """
        This handler receives messages with `/start` command
        """
        # Most event objects have aliases for API methods that can be called in events' context
        # For example if you want to answer to incoming message you can use `message.answer(...)` alias
        # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
        # method automatically or call API method directly via
        # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
        print(message.chat.id, message.text)
        await self._scheduler.handle_message(MessageDomain(
            str(message.chat.id),
            message.text
        ))
        await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

    async def echo_handler(self, message: types.Message) -> None:
        """
        Handler will forward receive a message back to the sender

        By default, message handler will handle all message types (like a text, photo, sticker etc.)
        """
        print(message.chat.id, message.text)
        await self._scheduler.handle_message(MessageDomain(
            str(message.chat.id),
            message.text
        ))
        try:
            # Send a copy of the received message
            await message.send_copy(chat_id=message.chat.id)
        except TypeError:
            # But not all the types is supported to be copied so need to handle it
            await message.answer("Nice try!")

    # async def send_message(self,
    #                        user_chat_id: str,
    #                        text: str,
    #                        message_type: types.Message.content_type,
    #                        keyboard_buttons: list[str],
    #                        keyboard_width: int,
    #                        save_previous_keyboard: bool):
    #     keyboard = self._create_keyboard(keyboard_buttons, keyboard_width, save_previous_keyboard)
    #
    #     await self._bot.send_message(
    #         user_chat_id,
    #         html.escape(text),
    #         reply_markup=keyboard,
    #         parse_mode=ParseMode.HTML
    #     )

    async def send_message(self,
                           chat_id: str,
                           text: str):
        await self._bot.send_message(chat_id, text)

    async def _create_keyboard(self, keyboard_buttons, keyboard_width, save_previous_keyboard):
        return
