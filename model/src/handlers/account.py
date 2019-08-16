import random

from PIL import Image
from io import BytesIO

from tornado.web import authenticated
from model.src.handlers import BaseAuthHandler


class AccountHandler(BaseAuthHandler):

    @authenticated
    async def get(self):
        await self.render("account.html", user = self.current_user)

    @authenticated
    async def post(self):
        file = self.request.files['file'][0]

        filename = file["filename"]
        if filename is None:
            filename = str(int(random.random() * 4294967295))

        user = self.current_user
        user_id = await self.get_user_id()
        if user_id is not None:
            user.picture = "data/" + filename

            image = Image.open(BytesIO(file['body']))
            image.save("static/" + user.picture, image.format)

            await self.conn.hset("users:" + str(user_id), "picture", user.picture)
