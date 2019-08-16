from pydoc import locate
from typing import Optional, List, Union

from model.src.connection import Connection


class Model:

    """ Name and Identifier are reserved for data persistence """
    key : Optional[int] = None
    identifier : Optional[str] = None

    def encode_model(self, default: str = "") -> List[str]:
        return Model.encode(self, default)

    @staticmethod
    def encode(obj: object, default: str = "") -> List[str]:
        encoding: List[str] = []

        for name in obj.__annotations__:
            if name != "key":
                value = getattr(obj, name, default)

                if isinstance(value, Model) and value.key is not None:
                    encoding.append(name)
                    encoding.append(str(value.key))
                else:
                    encoding.append(name)

                    value = getattr(obj, name, default)
                    if isinstance(value, bool):
                        encoding.append(str(int(value)))
                    else:
                        encoding.append(value)

        return encoding

    @classmethod
    async def decode_source(cls, source: dict, conn: Connection = None, lazy: bool = True, default: str = "") -> 'Model':
        obj = cls()

        for name in obj.__annotations__:
            if name in source:
                value = source[name]

                if value == default:
                    continue

                obj_attrib = getattr(obj, name, None)
                if isinstance(obj_attrib, Model) and not lazy:
                    attrib_class = locate("model.src.models." + obj_attrib.__class__.__name__)

                    if isinstance(attrib_class(), Model):
                        obj_attrib_value = await attrib_class.decode(conn, value, lazy, default)

                        setattr(obj, name, obj_attrib_value)
                    else:
                        raise Exception(f"Illegal argument: {attrib_class.__class__.name}, must extend Model class.")
                else:
                    try:
                        int(value)

                        setattr(obj, name, int(value))
                    except ValueError:
                        setattr(obj, name, value)

        return obj

    @classmethod
    async def decode(cls, conn, key: Optional[Union[int, str]], lazy: bool = False, default: str = "") -> 'Model':
        assert(conn is not None and isinstance(conn, Connection))
        assert(key is not None)

        source = await conn.hgetall(f"{cls.identifier}:{key}")

        return await cls.decode_source(source, conn, lazy, default)
