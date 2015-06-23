__author__ = 'gautam'


class BaseBackend(object):

    def __init__(self, table_name):
        super(BaseBackend, self).__init__()
        self.table_name = table_name

    def init(self):
        pass

    def get(self, env, key):
        pass

    def import_data(self, env, data_dict):
        pass

    def export_data(self, env):
        pass
