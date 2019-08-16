import jsonpickle

from tornado.web import authenticated

from typing import Optional

from model.src.handlers import BaseAuthHandler
from model.src.models import Reply, User

from tornado.escape import json_decode


class ChatifyHandler(BaseAuthHandler):

    body: Optional[dict]

    def base_prepare(self) -> None:
        if "application/json" in self.request.headers.get("Content-Type", ""):
            self.body = json_decode(self.request.body)
        else:
            self.body = None

    @authenticated
    async def get(self):
        search = self.get_query_argument("search", None)

        if search is not None:
            friends = [ friend for friend in await self.get_friends() if search in friend.name ]

            self.write(jsonpickle.encode(friends))
        else:
            await self.render("chatify.html", user = self.current_user, friends = await self.get_friends())

    @authenticated
    async def post(self):
        if self.body is not None:
            if "data" in self.body and "timestamp" in self.body and "recipient" in self.body:
                reply = Reply(self.current_user, self.body["recipient"], self.body["data"])

                print(self.body["data"])

        self.write("Success")

    async def get_friend(self, key) -> User:
        identifier = key[key.index(":") + 1:]

        return await User.decode(self.conn, identifier)

    async def get_friends(self):
        user_keys = await self.conn.keys("users:*")

        users = [ await self.get_friend(key) for key in user_keys ]

        return users
