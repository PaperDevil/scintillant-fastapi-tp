import os
import pathlib
import typing

import pickledb


class PickleDBCache:
    """ Easy way to get key-value storage without Redis """
    __pickledb: pickledb.PickleDB = None

    @classmethod
    def init_pickle_db(cls, db_filename: str = 'pickle.db'):
        cls.__pickledb = pickledb.load(pathlib.Path(os.getcwd() + db_filename), False)

    @classmethod
    def close_pickle_db(cls) -> bool:
        return cls.__pickledb.dump()

    @classmethod
    def exist(cls, key: str) -> bool:
        return cls.__pickledb.exists(key)

    @classmethod
    def set(cls, key: str, val: typing.Hashable) -> bool:
        return cls.__pickledb.set(key, val)

    @classmethod
    def get(cls, key: str) -> typing.Any:
        return cls.__pickledb.get(key)

    @classmethod
    def get_or_create(cls, key: str) -> typing.Any:
        if cls.exist(key):
            return cls.get(key)
        cls.set(key, {})
        return {}

    @classmethod
    def update(cls, key: str, val: typing.Hashable) -> bool:
        if cls.exist(key):
            data = cls.get(key)
            return cls.set(key, data | val)
        raise KeyError(f"Key '{key}' doesn't exist in pickle DB.")
