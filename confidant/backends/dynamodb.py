import logging
import uuid

from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.table import Table

from confidant.backends import BaseBackend, cache_manager

__author__ = 'gautam'


class DynamodbBackend(BaseBackend):
    def __init__(self, table_name, env, connection=None):
        self.__table_name = table_name
        self.__env = env
        self.__connection = connection
        self.__kwargs = dict(table_name=table_name)
        if connection:
            self.__kwargs['connection'] = connection
        self.__table = Table(**self.__kwargs)
        self.cache = cache_manager.get_cache(str(uuid.uuid4()), expires=3600)

    def initialize(self, read_throughput=1, write_throughput=1):
        kwargs = self.__kwargs.copy()
        kwargs['schema'] = [
            HashKey('key'),  # defaults to STRING data_type
            RangeKey('env'),
        ]
        kwargs['throughput'] = {
            'read': read_throughput,
            'write': write_throughput
        }
        return Table.create(**kwargs)

    def fetch_all(self):
        logging.info("Fetching all config from {} in {}".format(self.__env, self.__table_name))
        table_scan = self.__table.scan(env__eq=self.__env)
        data_dict = {}
        for item in table_scan:
            key, value = item['key'], item['val']
            data_dict[key] = value
            self.cache.set_value(key, value)
        return data_dict

    def __getattr__(self, item):
        return self.get(item)


    def set(self, key, value):
        try:
            self.__table.put_item({
                'key': key,
                'env': self.__env,
                'val': value
            }, overwrite=True)
            self.cache.set_value(key, value)
        except:
            logging.exception("Error setting value")
            raise

    def get(self, key):
        """
        Get a key from dynamodb backend
        :param env:
        :param key:
        :return:
        """
        if key in self.cache:
            return self.cache.get(key)
        else:
            value = self.__table.get_item(key=key, env=self.__env)
            self.cache.set_value(key, value)
            return value

    def import_data(self, env, data_dict):
        """
        Bulk import data into configuration table
        :param env: the environment to import into
        :param data_dict: dict data as key-value pairs, Data is expected to be flat
        :return: None
        """
        with self.__table.batch_write() as batch:
            for key, value in data_dict.iteritems():
                batch.put_item(data={
                    'env': env,
                    'key': key,
                    'val': value
                })

    def export_data(self):
        """
        Bulk Export data as dict
        :param env: the environment to export from
        :return: dict containing the data
        """
        return self.fetch_all()
