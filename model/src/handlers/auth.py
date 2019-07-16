from typing import Optional, Awaitable

from tornado.web import RequestHandler
from tornado.auth import FacebookGraphMixin


class AuthSignHandler(RequestHandler, FacebookGraphMixin):

    def initialize(self, connection):

        self.connection = connection

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):

        self.render("auth/auth_sign.html")


class AuthFacebookSignHandler(RequestHandler, FacebookGraphMixin):

    private_keys = [["access_token", "token"], ["session_expires", "expire"]]
    public_keys = ["email", "first_name", "last_name", "name"]

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self, connection):

        self.connection = connection

    async def get(self):
        if self.get_argument("code", None):
            user = await self.get_authenticated_user(
                redirect_uri = 'http://localhost:8000/auth/sign/facebook',
                client_id = self.settings["facebook_api_key"],
                client_secret = self.settings["facebook_secret"],
                code = self.get_argument("code"),
                extra_fields = dict({"email": None})
            )

            token = user.get("access_token", None)

            row = []
            for key in self.private_keys:
                row.extend([key[1], user.get(key[0], None)])

            row.extend(["password", ""])

            for key in self.public_keys:
                row.extend([key, user.get(key, None)])

            user_id = await self.connection.conn.incr("user_id")
            await self.connection.conn.hmset("users:" + str(user_id), *row)
            await self.connection.conn.hset("tokens", token, user_id)

            self.set_secure_cookie("token", token)
            self.redirect("/chatify", permanent = True)
        else:

            self.authorize_redirect(
                redirect_uri = 'http://localhost:8000/auth/sign/facebook',
                client_id = self.settings["facebook_api_key"],
                extra_params = {"scope" : ["email"]}
            )

    def options(self):
        self.set_status(204)
        self.finish()


class AuthLoginHandler(RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self, connection):

        self.connection = connection

    def get(self):

        self.render("auth/auth_sign.html")