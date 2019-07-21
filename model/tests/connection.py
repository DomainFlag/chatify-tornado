import unittest
import asyncio

from model.src.connection import Connection
from model.src.models import User


class RedisCommandTest(unittest.TestCase):

    def test_command(self):
        loop = asyncio.get_event_loop()
        conn = Connection.initialize_connection(loop)

        loop.run_until_complete(self.exec_redis_command(conn))

        loop.run_until_complete(conn.close_connection())
        loop.close()

    @staticmethod
    async def exec_redis_command(conn):
        """Redis command execution test"""
        value = await conn.hgetall("users:21")

        user = User()
        user.decode(user, value)

        print(user.__dict__)


if __name__ == '__main__':
    unittest.main()
