from beaker.util import parse_cache_config_options

__author__ = 'gautam'

from beaker.cache import CacheManager

cache_manager = CacheManager(**parse_cache_config_options({
    'cache.type': 'memory'
}))


class BaseBackend(object):
    def get(self, key):
        pass

    def __getattr__(self, item):
        return self.get(item)

    def initialize(self):
        """
        Initialize the backend if necessary
        :return:
        """
        pass

    def import_data(self, data_dict):
        pass

    def export_data(self):
        pass

    def set(self, key, value):
        pass


class BackendNotInitializedError(ValueError):
    pass
