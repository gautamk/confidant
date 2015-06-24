import logging

from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.table import Table

from confidant.backends import BaseBackend, cache_manager

__author__ = 'gautam'


class DynamodbBackend(BaseBackend):
    def __init__(self, table_name, env, connection=None):
        super(DynamodbBackend, self).__init__()
        self.table_name = table_name,
        self.env = env
        self.connection = connection
        self.kwargs = {}
        if self.connection:
            self.kwargs['connection'] = self.connection
        self.table = Table(table_name, **self.kwargs)

    def initialize(self, read_throughput=1, write_throughput=1):
        return Table.create(self.table_name, schema=[
            HashKey('key'),  # defaults to STRING data_type
            RangeKey('env'),
        ], throughput={
            'read': read_throughput,
            'write': write_throughput
        }, **self.kwargs)

    @cache_manager.cache('thecache', expires=3600)
    def fetch_all(self):
        logging.info("Fetching all config from {} in {}".format(self.env, self.table_name))
        table_scan = self.table.scan(env__eq=self.env)
        data_dict = {}
        for item in table_scan:
            data_dict[item['key']] = item['val']
        return data_dict

    def __getattr__(self, item):
        return self.get(item)

    def get(self, key):
        """
        Get a key from dynamodb backend
        :param env:
        :param key:
        :return:
        """
        data_dict = self.fetch_all()
        return data_dict.get(key)

    def import_data(self, env, data_dict):
        """
        Bulk import data into configuration table
        :param env: the environment to import into
        :param data_dict: dict data as key-value pairs, Data is expected to be flat
        :return: None
        """
        with self.table.batch_write() as batch:
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
