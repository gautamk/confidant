import random
import string
import unittest

from backends.dynamodb import DynamodbBackend

__author__ = 'gautam'


class TestDynamodbBackend(unittest.TestCase):
    def random_string(self):
        return ''.join(random.SystemRandom().choice(string.letters + string.digits) for _ in range(5))

    def setUp(self):
        self.backend = DynamodbBackend('test-db')

    def test_init(self):
        self.backend.init()

    def test_import_export(self):
        data_dict = {}
        env = self.random_string()
        for _ in range(100):
            data_dict[self.random_string()] = self.random_string()

        self.backend.import_data(env=env, data_dict=data_dict)
        exported_data = self.backend.export_data(env=env)
        self.assertDictEqual(data_dict, exported_data)
        with self.backend.table.batch_write() as batch:
            for key, value in data_dict.iteritems():
                batch.delete_item(key=key, env=env)
