import unittest
import asyncio

from model.src.connection import Connection
from model.src.models import User


class RedisCommandTest(unittest.TestCase):

    def test_command(self):
        conn = Connection.initialize_connection()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.exec_redis_command(conn))

        conn.release_connection()

    @staticmethod
    async def exec_redis_command(conn):
        """Redis command execution test"""
        keys = await conn.keys("users:*")

        print(keys)


if __name__ == '__main__':
    unittest.main()
