from typing import Optional
from model.src.models import Model, Picture


class User(Model):

    identifier = "users"

    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    picture: Optional[Picture] = Picture()

    token: Optional[str] = None
    expire: Optional[str] = None
