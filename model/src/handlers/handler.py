from typing import Optional, Awaitable, Union

from tornado.web import RequestHandler, Finish
from tornado.websocket import WebSocketHandler
from tornado import gen, escape

from model.src.connection import Connection
from model.src.models import Messenger, User


class BaseHandler(RequestHandler):

    conn: Connection

    def initialize(self, conn: Connection):
        self.conn = conn

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

    # async def prepare(self):
    #     """ middleware auth
    #
    #     Override for basic request handler
    #     :return:
    #     """""
    #
    #     user = await self.get_current_user()
    #     if not user:
    #         await self.redirect("/", permanent = True)
    #
    #         raise Finish()
    #     else:
    #         await self.base_prepare()

    def base_prepare(self) -> Optional[Awaitable[None]]:

        pass


class BaseAppHandler(BaseAuthHandler):

    mess: Messenger

    def initialize(self, conn: Connection, mess: Messenger):
        self.conn = conn
        self.mess = mess


class BaseSocketHandler(WebSocketHandler, BaseHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def on_message(self, message: Union[str, bytes]) -> Optional[Awaitable[None]]:
        raise NotImplementedError
