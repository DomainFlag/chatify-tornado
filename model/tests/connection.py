import unittest
import asyncio

from model.src.connection import Connection
from model.src.models import User


class RedisCommandTest(unittest.TestCase):

    def test_command(self):
        conn = Connection.initialize_connection()
        asyncio.run(self.exec_redis_command(conn))
        asyncio.run(conn.close_connection())

    @staticmethod
    async def exec_redis_command(conn):
        """Redis command execution test"""
        value = await conn.hgetall("users:21")

        user = User()
        user.decode(user, value)

        print(user.__dict__)


if __name__ == '__main__':
    unittest.main()
