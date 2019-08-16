import time


class Reply:

    author: object
    recipient: str
    content: str

    def __init__(self, author, recipient, content):

        self.author = author
        self.recipient = recipient
        self.content = content
        self.time = int(time.time())
