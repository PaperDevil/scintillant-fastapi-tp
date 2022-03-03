from typing import Optional
import databases

from app.schema.utils import get_url


class DatabaseDriver:

    _database: Optional[databases.Database] = None

    @classmethod
    def database(cls) -> databases.Database:
        if cls._database:
            return cls._database
        else:
            cls._database = databases.Database(get_url())
            return cls._database

    @classmethod
    async def init_primary_db(cls):
        if not cls.database().is_connected:
            await cls.database().connect()
        return cls.database()

    @classmethod
    async def close_primary_pool_db(cls) -> None:
        if cls.database().is_connected:
            await cls.database().disconnect()
