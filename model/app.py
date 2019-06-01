import tornado.ioloop
import tornado.web
import tornado.httpclient
import os
import model.src.handlers as handlers
import model.src.components as components

from tornado.web import Application, url
from model.src.models.messenger import Messenger

modules = {
    "ui_modules" : {
        "welcome" : components.Welcome,
        "message" : components.Message
    }
}

settings = {
    "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    "static_path" : os.path.join(os.path.dirname(__file__), "static"),
    "compiled_template_cache": False,
    "cookie_secret" : "fa421isn2142190sha893h81h42"
}


def create_app():

    # instance of messenger
    messenger = Messenger()

    return Application([
        url(r"/", handlers.WelcomeHandler),
        url(r"/main", handlers.MainHandler, dict({"messenger": messenger})),
        url(r"/user", handlers.UserHandler),
        url(r"/socket", handlers.MessageHandler, dict({"messenger" : messenger})),
        url(r"/chat/input", handlers.ChatHandler, dict({"messenger" : messenger}))
    ], ** settings, ** modules)


def run():
    app = create_app()
    app.listen(8000)

    tornado.ioloop.IOLoop.current().start()
