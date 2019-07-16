from model.src.handlers import BaseHandler
from model.src.models import Reply, User

import jsonpickle

class QueryHandler(BaseHandler):

    def prepare(self):
        pass

    def initialize(self, connection, messenger):

        self.connection = connection
        self.messenger = messenger

    async def get(self):

        res = None

        # for index in range(1000):
        #     await self.connection.conn.execute('lpush', 'values', index)
        res = await self.connection.conn.execute('lrange', 'values', '0', '-1')

        self.write(jsonpickle.encode(res))