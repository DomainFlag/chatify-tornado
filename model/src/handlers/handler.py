from typing import Optional, Awaitable, Union

from tornado.web import RequestHandler, Finish
from tornado.websocket import WebSocketHandler
from tornado import gen, escape

from model.src.connection import Connection
from model.src.models import Messenger, User


class BaseHandler(RequestHandler):

    conn: Optional[Connection]
    mess: Optional[Messenger]

    def initialize(self, conn: Optional[Connection] = None, mess: Optional[Messenger] = None):
        self.conn = conn
        self.mess = mess

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass


class BaseAuthHandler(BaseHandler):

    async def get_current_user(self) -> Optional[User]:
        token_raw = self.get_secure_cookie("token")
        if token_raw is None:
            return None

        token = escape.native_str(token_raw)
        if token is None:
            return None

        user_id = await self.conn.hget("tokens", token)
        if user_id is None:
            return None

        raw_user = await self.conn.hgetall("users:" + escape.native_str(user_id))

        user = User()
        user.decode(user, raw_user)

        return user


class BaseSocketHandler(WebSocketHandler, BaseAuthHandler):

    def on_message(self, message: Union[str, bytes]) -> Optional[Awaitable[None]]:
        raise NotImplementedError
