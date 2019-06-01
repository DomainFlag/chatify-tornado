from tornado.web import UIModule


class Message(UIModule):

    def css_files(self):

        return ["components\\message\\message.css"]

    def javascript_files(self):

        return ["components\\message\\message.js"]

    def render(self, user, message):

        style = {
            "direction" : "direction-lr" if user.__eq__(message.author) else "direction-rl"
        }

        return self.render_string("components\\message.html", message = message, style = style)
