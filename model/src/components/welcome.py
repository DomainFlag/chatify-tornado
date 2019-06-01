from tornado.web import UIModule


class Welcome(UIModule):

    def render(self):

        return self.render_string("welcome.html")
