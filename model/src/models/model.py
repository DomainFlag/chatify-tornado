from typing import List


class Model:

    @staticmethod
    def encode(obj: object, default: str = "") -> List[str]:
        encoding: List[str] = []

        for attr in obj.__dict__:
            encoding.append(attr)
            encoding.append(getattr(obj, attr, default))

        return encoding

    @staticmethod
    def decode(obj: object, source: dict):
        for attr in obj.__dict__:
            if attr in source:
                setattr(obj, attr, source[attr])
