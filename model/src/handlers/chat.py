from model.src.handlers import BaseHandler
from model.src.models import Reply, User


class ChatHandler(BaseHandler):

    def initialize(self, connection, messenger):

        self.connection = connection
        self.messenger = messenger

    def post(self):

        message_input = self.get_body_argument("message-input", default = None)

        if message_input is not None:

            user = User()

            reply = Reply(user, message_input)

            self.messenger.replies.append(reply)

            self.redirect("/", permanent = True)