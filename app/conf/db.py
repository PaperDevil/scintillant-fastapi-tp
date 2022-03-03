from app.external.utils.conf import ConfigUtils

PICKLE_CACHE_DB_NAME = ConfigUtils.env('PICKLE_CACHE_DB_NAME', str, default='pickle.db')
