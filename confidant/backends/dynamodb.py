import logging
import uuid
from decimal import Decimal

import six
from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.table import Table
from boto.exception import JSONResponseError

from confidant.backends import BaseBackend, cache_manager, BackendNotInitializedError

__author__ = 'gautam'


def _simplify_types(value):
    _type = type(value)
    if _type == Decimal:
        return float(value) if '.' in str(value) else int(value)
    elif _type == dict:
        simple_values = {}
        for key, val in six.iteritems(value):
            simple_values[key] = _simplify_types(val)
        return simple_values
    elif _type == list:
        simple_values = []
        for item in value:
            simple_values.append(_simplify_types(item))
        return simple_values
    return value


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
            key, value = item['key'], _simplify_types(item['val'])
            data_dict[key] = value
            self.cache.set_value(key, value)
        return data_dict

    def set(self, key, value):
        try:
            self.__table.put_item({
                'key': key,
                'env': self.__env,
                'val': value
            }, overwrite=True)
            self.cache.set_value(key, value)
        except JSONResponseError as e:
            if e.body.get('Message') == 'Cannot do operations on a non-existent table':
                raise BackendNotInitializedError("Unable to decode file, Try calling the initialize method", e)
            raise e

    def get(self, key):
        """
        Get a key from dynamodb backend
        :param key:
        :return:
        """
        if key in self.cache:
            return self.cache.get(key)
        else:
            try:
                value_item = self.__table.get_item(key=key, env=self.__env)
                value = _simplify_types(value_item['val'])
                self.cache.set_value(key, value)
                return value
            except JSONResponseError as e:

                if e.body.get('Message') == 'Cannot do operations on a non-existent table':
                    raise BackendNotInitializedError("Unable to decode file, Try calling the initialize method", e)
                raise e

    def import_data(self, data_dict):
        """
        Bulk import data into configuration table
        :param data_dict: dict data as key-value pairs, Data is expected to be flat
        :return: None
        """
        with self.__table.batch_write() as batch:
            for key, value in six.iteritems(data_dict):
                batch.put_item(data={
                    'env': self.__env,
                    'key': key,
                    'val': value
                })

    def export_data(self):
        """
        Bulk Export data as dict
        :return: dict containing the data
        """
        return self.fetch_all()
