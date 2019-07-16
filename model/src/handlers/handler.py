from typing import Optional, Awaitable, Union

from tornado.web import RequestHandler, Finish
from tornado.websocket import WebSocketHandler
from tornado import gen, escape


class BaseHandler(RequestHandler):

    def initialize(self, connection):
        self.connection = connection

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    @gen.coroutine
    def get_current_user(self):
        token_raw = self.get_secure_cookie("token")
        token = escape.native_str(token_raw)

        user_id = yield self.connection.conn.hget("tokens", token)
        user = yield self.connection.conn.hgetall("users:" + escape.native_str(user_id))

        return user

    async def prepare(self):
        """ middleware auth
        
        Override for basic request handler
        :return: 
        """""

        user = await self.get_current_user()
        if not user:
            await self.redirect("/", permanent = True)

            raise Finish()
        else:
            await self.base_prepare()

    def base_prepare(self) -> Optional[Awaitable[None]]:

        pass


class BaseSocketHandler(WebSocketHandler, BaseHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:

        pass

    def on_message(self, message: Union[str, bytes]) -> Optional[Awaitable[None]]:

        raise NotImplementedError
