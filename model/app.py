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
    "facebook_secret" : configuration["facebook_secret"],
    "default_handler_class" : handlers.NotFoundHandler
}


def create_app():

    conn = Connection.initialize_connection()
    mess = Messenger()

    bundle_bare_mode = dict({"conn": conn})
    bundle_auth_mode = dict({"conn": conn, "mess": mess})

    return Application([
        url(r"/", handlers.WelcomeHandler, bundle_bare_mode),
        url(r"/auth/sign", handlers.AuthSignHandler, bundle_bare_mode),
        url(r"/auth/sign/facebook", handlers.AuthFacebookSignHandler, bundle_bare_mode),
        url(r"/auth/login", handlers.AuthLoginHandler, bundle_bare_mode),
        url(r"/auth/logout", handlers.AuthLogoutHandler, bundle_bare_mode),
        url(r"/chatify", handlers.MainHandler, bundle_auth_mode),
        url(r"/user", handlers.UserHandler),
        url(r"/socket", handlers.MessageHandler, bundle_auth_mode),
        url(r"/chat/input", handlers.ChatHandler, bundle_auth_mode)
    ], ** settings, ** modules)


def run():
    app = create_app()
    app.listen(8000)

    tornado.ioloop.IOLoop.current().start()
