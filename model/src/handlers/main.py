from model.src.handlers import BaseHandler


class MainHandler(BaseHandler):

    def initialize(self, connection, messenger):

        self.connection = connection
        self.messenger = messenger

    def prepare(self):
        pass

    def get(self):

        self.render("main.html", user = self.get_user(), replies = self.messenger.replies)

    def post(self):

        print(self.get_body_argument("form-input-content"))
