import tornado.ioloop
import tornado.web
import tornado.httpclient
import os
import model.src.handlers as handlers
import model.src.modules as modules
import aioredis
import asyncio

from tornado.web import Application, url
from model.src.models.messenger import Messenger

modules = {
    "ui_modules" : {
        "welcome" : modules.Welcome,
        "message" : modules.Message
    }
}

settings = {
    "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    "static_path" : os.path.join(os.path.dirname(__file__), "static"),
    "compiled_template_cache": False,
    "cookie_secret" : "fa421isn2142190sha893h81h42"
}


def create_app():

    connection = Connection()
    messenger = Messenger()

    bundle = dict({"connection": connection, "messenger": messenger})

    return Application([
        url(r"/", handlers.WelcomeHandler),
        url(r"/index", handlers.MainHandler, bundle),
        url(r"/query", handlers.QueryHandler, bundle),
        url(r"/user", handlers.UserHandler),
        url(r"/socket", handlers.MessageHandler, bundle),
        url(r"/chat/input", handlers.ChatHandler, bundle)
    ], ** settings, ** modules)


class Connection:

    def __init__(self):

        pass
        # self.loop = asyncio.get_event_loop()
        # self.conn = self.loop.run_until_complete(self.create_connection())

    # async def create_connection(self):
    #
    #     return await aioredis.create_connection('redis://localhost', loop = self.loop)

    def close_connection(self):

        pass
        # self.conn.close()
        # self.loop.run_until_complete(self.conn.wait_closed())


def run():
    app = create_app()
    app.listen(8000)

    tornado.ioloop.IOLoop.current().start()
