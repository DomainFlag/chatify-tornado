from typing import Optional
from model.src.models import Model


class Picture(Model):

    identifier = "pictures"

    url: Optional[str] = None
    local: bool = False
    width: Optional[int] = None
    height: Optional[int] = None
