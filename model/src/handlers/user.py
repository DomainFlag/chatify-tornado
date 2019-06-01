import json

from model.src.handlers import BaseHandler


class UserHandler(BaseHandler):

    def get(self):

        # get the current logged in user
        user = self.get_user()

        # json response
        response = json.dumps(user.__dict__)

        self.write(response)