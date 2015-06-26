import random
import uuid

from boto.dynamodb2.layer1 import DynamoDBConnection
import six

from confidant.backends import BackendNotInitializedError
from confidant.backends.dynamodb import DynamodbBackend
from confidant.tests import BaseTest

__author__ = 'gautam'


class TestDaynamodbBackend(BaseTest):
    def setUp(self):
        super(TestDaynamodbBackend, self).setUp()
        self.conn = DynamoDBConnection(
            host='localhost',
            port=8000,
            aws_access_key_id='anything',
            aws_secret_access_key='anything',
            is_secure=False)
        self.backend = DynamodbBackend(self.random_string(), self.random_string(), connection=self.conn)
        self.backend.initialize()

    def test_get(self):
        self.backend.set('TEST', 'TEST')
        self.assertEquals(self.backend.get('TEST'), 'TEST')

    def test_set(self):
        random_data = [
            "RandomString",
            1231,
            {
                'test_string': 'kajshdkahs'
            },
            [
                18230,
                18728
            ]
        ]
        key = str(uuid.uuid4())
        value = random.choice(random_data)
        self.backend.set(key, value)
        self.assertEquals(value, self.backend.get(key))

    def test_attrs(self):
        random_value = str(uuid.uuid4())
        self.backend.set('RANDOM_VALUE', random_value)
        self.assertEquals(self.backend.RANDOM_VALUE, random_value)
        self.assertEquals(self.backend.get('RANDOM_VALUE'), random_value)

    def test_import(self):
        data_dict = self.random_dict()
        self.backend.import_data(data_dict)
        for k, v in six.iteritems(data_dict):
            self.assertEqual(self.backend.get(k), v)

    def test_export(self):
        data_dict = self.random_dict()
        self.backend.import_data(data_dict)
        self.assertDictEqual(self.backend.export_data(), data_dict)

    def test_get_uninitialized(self):
        backend = DynamodbBackend(self.random_string(), self.random_string(), connection=self.conn)
        with self.assertRaises(BackendNotInitializedError):
            backend.get('TEST')

    def test_set_uninitialized(self):
        backend = DynamodbBackend(self.random_string(), self.random_string(), connection=self.conn)
        with self.assertRaises(BackendNotInitializedError):
            backend.set('TEST', 'TEST')
