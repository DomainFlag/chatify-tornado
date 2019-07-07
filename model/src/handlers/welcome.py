from typing import Optional, Awaitable
from model.src.handlers import BaseHandler
import tornado.ioloop
import asyncio
import time
import tornado.web
from tornado import gen
from tornado.ioloop import IOLoop


class WelcomeHandler(BaseHandler):

    def prepare(self):
        pass

    def get(self):

        self.render("welcome.html")