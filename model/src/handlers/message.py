from model.src.handlers import BaseSocketHandler


class MessageHandler(BaseSocketHandler):

    def initialize(self, connection, messenger):

        self.connection = connection
        self.messenger = messenger

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        print(message)

        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")
