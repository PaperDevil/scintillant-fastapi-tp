import sys
import os

import json
from loguru import logger
from fastapi import FastAPI, Request

from app.conf.server import (
    DEBUG, TITLE_API,
    DESCRIPTION_API, VERSION_API
)
from app.internal.drivers.picklecache import PickleDBCache
from app.internal.web.api import general_router


class FastAPIServer:

    @staticmethod
    def get_app() -> FastAPI:
        logger.add(sys.stderr, level='INFO')

        app = FastAPI(
            debug=DEBUG,
            title=TITLE_API,
            description=DESCRIPTION_API,
            version=VERSION_API,
            docs_url='/swagger',
            openapi_url='/openapi.json'
        )

        app.include_router(general_router)

        @app.on_event('startup')
        async def initials():
            PickleDBCache.init_pickle_db()

        @app.on_event('shutdown')
        async def closes():
            PickleDBCache.close_pickle_db()

        @app.get('/snlt')
        async def config(request: Request):
            with open(os.getcwd() + '/.snlt') as snlt:
                data = json.load(snlt)
            return data

        return app
