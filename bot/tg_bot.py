import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from domain.scheduler import Scheduler
from domain.storage import Storage
from secret_env import BOT_TOKEN
from bot.behavior import Behavior


TOKEN = BOT_TOKEN


class TGBot:

    def __init__(self, token: str, parse_mode: ParseMode = ParseMode.HTML):
        self._bot = Bot(token, parse_mode=parse_mode)
        self._dp = Dispatcher()
        self._storage = Storage()

        self._behavior = Behavior(self._dp, self._bot, self._storage)
        self._behavior.configure()

    async def start(self):
        await self._storage.start()
        await self._dp.start_polling(self._bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    tg_bot = TGBot(TOKEN)
    asyncio.run(tg_bot.start())
