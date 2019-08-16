from typing import Optional, Awaitable, Union

from tornado.web import RequestHandler, Finish
from tornado.websocket import WebSocketHandler
from tornado import escape

from model.src.connection import Connection
from model.src.models import Messenger, User

import jsonpickle


class BaseHandler(RequestHandler):

    conn: Optional[Connection]
    mess: Optional[Messenger]

    def initialize(self, conn: Optional[Connection] = None, mess: Optional[Messenger] = None):
        self.conn = conn
        self.mess = mess

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass


class BaseAuthHandler(BaseHandler):

    async def prepare(self) -> Optional[Awaitable[None]]:
        if self.current_user is not None:
            return

        user_id = await self.get_user_id()
        if user_id is None:
            return

        self.current_user = await User.decode(self.conn, user_id)
        self.base_prepare()

    def base_prepare(self) -> None:
        pass

    async def get_user_id(self):
        token_raw = self.get_secure_cookie("token")
        if token_raw is None:
            return None

        token = escape.native_str(token_raw)
        return await self.conn.hget("tokens", token)


class BaseSocketHandler(WebSocketHandler, BaseAuthHandler):

    def on_message(self, message: Union[str, bytes]) -> Optional[Awaitable[None]]:
        raise NotImplementedError
