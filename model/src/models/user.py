from typing import Optional
from model.src.models import Model


class User(Model):

    name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]

    token: Optional[str]
    expire: Optional[str] = None

    def __init__(self):
        super().__init__()

        self.name = None
        self.first_name = None
        self.last_name = None
        self.email = None
        self.token = None
        self.expire = None
