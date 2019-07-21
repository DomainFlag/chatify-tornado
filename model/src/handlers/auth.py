from tornado.auth import FacebookGraphMixin

from model.src.handlers import BaseHandler, BaseAuthHandler

import bcrypt
import uuid


class AuthMessage:

    AUTH_SIGN: str = "sign"
    AUTH_LOGIN: str = "login"

    auth_mode: str
    mode: str
    redirect: str
    redirection: str
    redirection_mode: str

    def __init__(self, auth_mode):

        self.auth_mode = auth_mode
        auth_sign: bool = self.auth_mode == AuthMessage.AUTH_SIGN

        self.mode = "sign up" if auth_sign else "login"
        self.redirect = "login" if auth_sign else "sign"
        self.redirection = "already have an account?" if auth_sign else "don't have an account, yet?"
        self.redirection_mode = "login" if auth_sign else "sign up"


class AuthSignHandler(BaseAuthHandler):

    auth = AuthMessage(AuthMessage.AUTH_SIGN)

    async def get(self):
        user = await self.get_current_user()

        await self.render("auth.html", auth = self.auth, user = user)

    async def post(self):
        email = self.get_body_argument("email", None)

        if email is not None:
            result = await self.conn.hget("emails", email)
            if result == 0:
                self.write("login name is already taken")

                return

        password = self.get_body_argument("password", None)

        if password is None:
            self.write("no empty password is allowed")
            await self.flush()

            return

        salt = bcrypt.gensalt(8)
        hash = bcrypt.hashpw(password.encode(), salt)

        row = ["email", email, "password", hash]
        token = uuid.uuid4().hex

        user_id = await self.conn.incr("user_id")
        await self.conn.hmset("users:" + str(user_id), *row)
        await self.conn.hset("tokens", token, user_id)
        await self.conn.hset("emails", email, user_id)

        self.set_secure_cookie("token", token)
        self.redirect("/chatify", permanent = True)


class AuthFacebookSignHandler(BaseHandler, FacebookGraphMixin):

    private_keys = [["access_token", "token"], ["session_expires", "expire"]]
    public_keys = ["email", "first_name", "last_name", "name"]

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

            user_id = await self.conn.incr("user_id")
            await self.conn.hmset("users:" + str(user_id), *row)
            await self.conn.hset("tokens", token, user_id)

            email = user.get("email", None)
            if email is not None:
                await self.conn.hset("emails", email, user_id)

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


class AuthLoginHandler(BaseAuthHandler):

    auth = AuthMessage(AuthMessage.AUTH_LOGIN)

    async def get(self):
        user = await self.get_current_user()

        await self.render("auth.html", auth = self.auth, user = user)

    async def post(self):
        email = self.get_body_argument("email", None)
        password = self.get_body_argument("password", None)

        if email is None or password is None:
            self.write("email or password is required")

            return

        raw_user_id: bytes = await self.conn.hget("emails", email)
        if raw_user_id is None:
            self.write("email or password is invalid")

            return

        user_id = int(raw_user_id.decode("utf-8"))

        raw_user_password: bytes = await self.conn.hget("users:" + str(user_id), "password")
        if raw_user_password is None:
            """Social authentication"""
            pass

        valid_user: bool = bcrypt.checkpw(password, raw_user_password.decode("utf-8"))
        if valid_user:
            raw_user_token = await self.conn.hget("users:" + str(user_id), "token")

            if raw_user_token is None:
                user_token = uuid.uuid4().hex
                await self.conn.hset("users:" + str(user_id), "token", user_token)
                await self.conn.hset("tokens", user_token, user_id)
            else:
                user_token = raw_user_token.decode("utf-8")

            self.set_secure_cookie("token", user_token)
            self.redirect("/chatify", permanent = True)
        else:
            self.write("email or password is invalid")


class AuthLogoutHandler(BaseAuthHandler):

    async def get(self):
        user = await self.get_current_user()
        if user is None:
            self.write("you are not authenticated yet")

            return

        self.conn.hdel("tokens", self.get_secure_cookie("token"))

        self.clear_cookie("token")
        self.redirect("/", permanent = True)
