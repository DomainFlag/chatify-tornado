import aioredis
import asyncio

from aioredis import Redis


class Connection:

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.conn = self.loop.run_until_complete(self.create_connection())

    async def create_connection(self) -> Redis:
        return await aioredis.create_redis('redis://localhost', loop = self.loop)

    async def close_connection(self):
        self.conn.close()
        await self.conn.wait_closed()