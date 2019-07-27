from model.src.handlers import BaseHandler


class NotFoundHandler(BaseHandler):

    def get(self):
        self.render("error.html")
