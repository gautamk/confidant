from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.table import Table

from .base_backend import BaseBackend

__author__ = 'gautam'


class DynamodbBackend(BaseBackend):
    def __init__(self, table_name):
        super(DynamodbBackend, self).__init__(table_name)
        self.table = Table(table_name)

    def init(self, read_throughput=1, write_throughput=1):
        return Table.create(self.table_name, schema=[
            HashKey('key'),  # defaults to STRING data_type
            RangeKey('env'),
        ], throughput={
            'read': read_throughput,
            'write': write_throughput
        })

    def get(self, env, key):
        """
        Get a key from dynamodb backend
        :param env:
        :param key:
        :return:
        """
        item = self.table.get_item(key=key, env=env)
        return item['val']

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

    def export_data(self, env):
        """
        Bulk Export data as dict
        :param env: the environment to export from
        :return: dict containing the data
        """
        table_scan = self.table.scan(env__eq=env)
        data_dict = {}
        for item in table_scan:
            data_dict[item['key']] = item['val']
        return data_dict


def init(table_name):
    return DynamodbBackend(table_name)
