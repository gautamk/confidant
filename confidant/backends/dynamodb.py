import logging

from boto.dynamodb2.table import Table

__author__ = 'gautam'


class BackendRenderer:
    def __init__(self, table_name, **kwargs):
        """
        :param table_name: The table name to query
        :param kwargs: filter argument for the table scan
        :return:
        """
        logging.debug("[Dynamodb] rendering from table {}".format(table_name))
        self.table = Table(table_name)
        self.table_data = {d['key']: d['value'] for d in self.table.scan(**kwargs)}

    def get(self, key):
        print self.table_data.get(key)
