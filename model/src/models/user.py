from typing import Optional
from model.src.models import Model


class User(Model):

    name: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]

    picture: Optional[str] = None

    token: Optional[str]
    expire: Optional[str]
