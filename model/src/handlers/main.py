from tornado.web import authenticated
from model.src.handlers import BaseAuthHandler, BaseHandler
from model.src.connection import Connection
from model.src.models import Messenger


class MainHandler(BaseHandler):

    mess: Messenger

    def initialize(self, conn: Connection, mess: Messenger):
        super().initialize(conn)

        self.mess = mess

    @authenticated
    def get(self):
        self.render("main.html")

    @authenticated
    def post(self):
        print(self.get_body_argument("form-input-content"))
