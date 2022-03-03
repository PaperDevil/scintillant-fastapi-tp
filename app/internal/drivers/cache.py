import json
from typing import Union, Optional

import aioredis


class CacheDriver:

    __redis: Optional[aioredis.Redis] = None

    @classmethod
    async def get(cls, key: Union[int, str]) -> Optional[dict]:
        key_exist: bool = await cls.__redis.exists(key)
        if key_exist:
            data = await cls.__redis.get(key)
            return json.loads(data)
        return {}

    @classmethod
    async def set(cls, key: Union[int, str], val: dict) -> None:
        data = json.dumps(val)
        await cls.__redis.set(key, data)

    @classmethod
    async def update(cls, key: Union[int, str], val: dict) -> None:
        data = await cls.get(key)
        if len(data) == 0:
            raise KeyError(f'Key {key} not found in cache!')
        data.update(val)
        await cls.set(key, data)

    @classmethod
    async def set_or_update(cls, key: Union[int, str], val: dict) -> None:
        try:
            await cls.update(key, val)
        except KeyError:
            await cls.set(key, val)
        except Exception:
            raise

    @classmethod
    async def init_redis_connection(cls, host, port, password) -> None:
        cls.__redis = await aioredis.from_url(f"redis://{host}:{port}/{0}", password=password)
        await cls.__redis.ping()

    @classmethod
    async def close_redis_connection(cls) -> None:
        await cls.__redis.close()
