from .handler import BaseAuthHandler


class WelcomeHandler(BaseAuthHandler):

    async def get(self):
        await self.render("welcome.html", user_auth = self.current_user is not None)
