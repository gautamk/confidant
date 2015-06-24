from beaker.util import parse_cache_config_options

__author__ = 'gautam'

from beaker.cache import CacheManager

cache_manager = CacheManager(**parse_cache_config_options({
    'cache.type': 'memory'
}))


class BaseBackend(object):
    @cache_manager.cache('thecache', expire=3600)
    def get(self, key):
        return key

    def initialize(self):
        """
        Initialize the backend if necessary
        :return:
        """
        raise NotImplementedError()
