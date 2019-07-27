import jsonpickle

from model.src.handlers import BaseHandler


class UserHandler(BaseHandler):

    def get(self):
        user = self.get_current_user()

        self.write(jsonpickle.encode(user))
