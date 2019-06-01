from typing import Optional, Awaitable
from model.src.handlers import BaseHandler


class WelcomeHandler(BaseHandler):

    def prepare(self):

        # authenticated process not required
        self.redirect_auth()

    def get(self):

        self.render("welcome.html")
