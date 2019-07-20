import unittest
import asyncio

from model.src.connection import Connection


class RedisCommandTest(unittest.TestCase):

    def test_command(self):
        self.conn = Connection()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.exec_redis_command())
        loop.run_until_complete(self.conn.close_connection())
        loop.close()

    async def exec_redis_command(self):
        # aioredis command output testing
        value = await self.conn.conn.sismember("names", "Jane")
        print(value)
        print(type(value))


if __name__ == '__main__':
    unittest.main()
