from .handler import BaseAuthHandler


class WelcomeHandler(BaseAuthHandler):

    async def get(self):
        user = await self.get_current_user()

        await self.render("welcome.html", user_auth = user is not None)
