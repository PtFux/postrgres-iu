from repositories.base.base_repository import BaseRepository


class BotScheduler:
    def __init__(self, repository: BaseRepository):
        self._repository = repository

    async def start(self):
        await self._repository.initialize()
