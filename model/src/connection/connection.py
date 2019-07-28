from abc import ABC

import aioredis
import asyncio

from asyncio import AbstractEventLoop
from aioredis import Redis


class Connection(Redis, ABC):

    authority: str = "redis://localhost"

    @staticmethod
    def initialize_connection(loop: AbstractEventLoop = None) -> 'Connection':
        if loop is None:
            loop = asyncio.get_event_loop()

        return loop.run_until_complete(Connection.create_connection(loop))

    @staticmethod
    async def create_connection(loop) -> Redis:
        # charset = "utf-8", decode_responses = True
        return await aioredis.create_redis(Connection.authority, loop = loop, commands_factory = Connection,
                                           encoding = "utf-8")

    def release_connection(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.close_connection())

    async def close_connection(self) -> None:
        self.close()

        await self.wait_closed()
