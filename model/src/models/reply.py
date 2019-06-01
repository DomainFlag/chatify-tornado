from time import gmtime, strftime


class Reply:

    def __init__(self, author, content):

        self.author = author
        self.content = content
        self.time = strftime("%M:%S", gmtime())