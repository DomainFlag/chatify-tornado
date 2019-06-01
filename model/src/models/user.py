import json


class User(json.JSONEncoder):

    def __init__(self):
        super().__init__()

        self.name = "DomainFlag"
        self.profile = "https://i0.wp.com/www.winhelponline.com/blog/wp-content/uploads/2017/12/user.png"

    def default(self, o):

        return o.__dict__
