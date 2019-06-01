from typing import Optional, Awaitable, Union

from tornado.web import RequestHandler, Finish
from tornado.websocket import WebSocketHandler


class BaseHandler(RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def prepare(self):
        """ middleware auth
        
        Override for basic request handler
        :return: 
        """""

        # get current authenticated user
        user = self.get_user()

        if user is None:

            # authentication required
            self.redirect("/", permanent = True)

            raise Finish()

        self.base_prepare()

    def base_prepare(self) -> Optional[Awaitable[None]]:

        pass

    def get_user(self):

        return None

    def redirect_auth(self):

        # get current authenticated user
        user = self.get_user()

        if user is not None:

            # authentication passed
            self.redirect("/main", permanent = True)


class BaseSocketHandler(WebSocketHandler, BaseHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:

        pass

    def on_message(self, message: Union[str, bytes]) -> Optional[Awaitable[None]]:

        raise NotImplementedError
