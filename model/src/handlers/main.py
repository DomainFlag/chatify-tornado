from tornado.web import authenticated
from model.src.handlers import BaseAuthHandler


class MainHandler(BaseAuthHandler):

    @authenticated
    async def get(self):
        user = await self.get_current_user()

        await self.render("main.html", user = user, friends = [])

    @authenticated
    def post(self):
        print(self.get_body_argument("form-input-content"))
