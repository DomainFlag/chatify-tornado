from typing import List


class Model:
    @staticmethod
    def encode(obj: object, default: str = "") -> List[str]:
        encoding: List[str] = []

        for name in obj.__annotations__:
            encoding.append(name)
            encoding.append(getattr(obj, name, default))

        return encoding

    @classmethod
    def decode(cls, source: dict, default: str = "") -> 'Model':
        obj = cls()

        for name in obj.__annotations__:
            if name in source:
                value = source[name]

                if value != default:
                    setattr(obj, name, value)

        return obj
