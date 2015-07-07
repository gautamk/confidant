import random
import uuid
from decimal import Decimal

from boto.dynamodb2.layer1 import DynamoDBConnection
import six

from confidant.backends import BackendNotInitializedError
from confidant.backends.dynamodb import DynamodbBackend, _simplify_types
from confidant.tests import BaseTest

__author__ = 'gautam'


class TestSimplifyTypes(BaseTest):
    def test_simplify_dict(self):
        test_data = {
            "k1": {
                "k2": Decimal(123)
            }
        }
        self.assertEquals(123, _simplify_types(test_data)['k1']['k2'])

    def test_simplify_list(self):
        test_data = [[["something", Decimal(123.3)]]]
        self.assertEqual(["something", 123.3], _simplify_types(test_data)[0][0])

    def test_complex_list(self):
        test_data = {
            "l1": [{
                "l2": [Decimal(432.33), Decimal(423)]
            }]
        }
        simplified_data = _simplify_types(test_data)
        val1 = simplified_data['l1'][0]['l2'][0]
        val2 = simplified_data['l1'][0]['l2'][1]
        self.assertTrue(type(val1) == float)
        self.assertTrue(type(val2) == int)
        self.assertEqual(val1, 432.33)
        self.assertEqual(val2, 423)

    def test_simple_decimal(self):
        self.assertEqual(1234, _simplify_types(Decimal(1234)))
        self.assertEqual(1234.1232, _simplify_types(Decimal(1234.1232)))
        self.assertTrue(type(_simplify_types(Decimal(23))) == int)
        self.assertTrue(type(_simplify_types(Decimal(23.232))) == float)


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
        self.assertEqual(value, self.backend.get(key))

    def test_attrs(self):
        random_value = str(uuid.uuid4())
        self.backend.set('RANDOM_VALUE', random_value)
        self.assertEqual(self.backend.RANDOM_VALUE, random_value)
        self.assertEqual(self.backend.get('RANDOM_VALUE'), random_value)

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
