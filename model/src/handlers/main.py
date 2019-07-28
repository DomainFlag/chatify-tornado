from tornado.web import authenticated

from model.src.handlers import BaseAuthHandler
from model.src.models import User


class MainHandler(BaseAuthHandler):

    @authenticated
    async def get(self):
        await self.render("main.html", user = self.current_user, friends = await self.get_friends())

    @authenticated
    def post(self):
        print(self.get_body_argument("form-input-content"))

    async def get_friend(self, key) -> User:
        user_raw = await self.conn.hgetall(key)

        return User.decode(user_raw)

    async def get_friends(self):
        user_keys = await self.conn.keys("users:*")

        users = [ await self.get_friend(key) for key in user_keys ]

        return users
