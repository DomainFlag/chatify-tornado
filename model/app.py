import tornado.ioloop
import tornado.web
import tornado.httpclient
import os
import model.src.handlers as handlers
import model.src.modules as modules

from tornado.web import Application, url
from model.src.models.messenger import Messenger
from model.src.connection import Connection

from .config import configuration


modules = {
    "ui_modules" : {
        "welcome" : modules.Welcome,
        "message" : modules.Message
    }
}

settings = {
    "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    "static_path" : os.path.join(os.path.dirname(__file__), "static"),
    "compiled_template_cache" : False,
    "debug" : True,
    "login_url" : "/auth/login",
    "cookie_secret" : configuration["cookie_secret"],
    "facebook_api_key" : configuration["facebook_api_key"],
    "facebook_secret" : configuration["facebook_secret"]
}


def create_app():

    conn = Connection.initialize_connection()
    mess = Messenger()

    bundle = dict({"conn": conn, "mess": mess})

    return Application([
        url(r"/", handlers.WelcomeHandler, {"conn": conn}),
        url(r"/auth/sign", handlers.AuthSignHandler, {"conn": conn}),
        url(r"/auth/sign/facebook", handlers.AuthFacebookSignHandler, {"conn": conn}),
        url(r"/auth/login", handlers.AuthLoginHandler, {"conn": conn}),
        url(r"/auth/logout", handlers.AuthLogoutHandler, {"conn": conn}),
        url(r"/chatify", handlers.MainHandler, bundle),
        url(r"/query", handlers.QueryHandler, bundle),
        url(r"/user", handlers.UserHandler),
        url(r"/socket", handlers.MessageHandler, bundle),
        url(r"/chat/input", handlers.ChatHandler, bundle)
    ], ** settings, ** modules)


def run():
    app = create_app()
    app.listen(8000)

    tornado.ioloop.IOLoop.current().start()
