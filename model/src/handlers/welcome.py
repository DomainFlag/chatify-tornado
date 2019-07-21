from typing import Optional, Awaitable
from tornado.web import RequestHandler
from .handler import BaseAuthHandler


class WelcomeHandler(BaseAuthHandler):

    async def get(self):
        user_auth = await self.get_current_user() is not None

        await self.render("welcome.html", user_auth = user_auth)
