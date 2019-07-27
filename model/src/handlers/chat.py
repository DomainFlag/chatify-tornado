from model.src.handlers import BaseAuthHandler
from model.src.models import Reply, User


class ChatHandler(BaseAuthHandler):

    def post(self):

        message_input = self.get_body_argument("message-input", default = None)

        if message_input is not None:

            user = User()

            reply = Reply(user, message_input)

            self.mess.replies.append(reply)

            self.redirect("/", permanent = True)