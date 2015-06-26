import random
import string
import unittest
import uuid

from boto.dynamodb2.layer1 import DynamoDBConnection

from confidant.backends.dynamodb import DynamodbBackend

__author__ = 'gautam'


class TestDaynamodbBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestDaynamodbBackend, cls).setUpClass()
        # Connect to DynamoDB Local
        cls.conn = DynamoDBConnection(
            host='localhost',
            port=8000,
            aws_access_key_id='anything',
            aws_secret_access_key='anything',
            is_secure=False)
        cls.backend = DynamodbBackend('testdb', 'prd', connection=cls.conn)
        cls.backend.initialize()
        cls.backend.set('TEST', 'TEST')

    def setUp(self):
        super(TestDaynamodbBackend, self).setUp()
        self.backend = self.__class__.backend
        self.conn = self.__class__.conn

    def test_get(self):
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

    def __random_string(self):
        max_len = random.randint(1, 100)
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in xrange(max_len))

    def __generate_random_dict(self):
        max_len = random.randint(1, 100)
        return {self.__random_string(): self.__random_string() for _ in xrange(max_len)}

    def test_import(self):
        backend = DynamodbBackend(self.__random_string(), self.__random_string(), connection=self.conn)
        backend.initialize()
        data_dict = self.__generate_random_dict()
        backend.import_data(data_dict)
        for k, v in data_dict.iteritems():
            self.assertEqual(backend.get(k), v)

    def test_export(self):
        backend = DynamodbBackend(self.__random_string(), self.__random_string(), connection=self.conn)
        backend.initialize()
        data_dict = self.__generate_random_dict()
        backend.import_data(data_dict)
        self.assertDictEqual(backend.export_data(), data_dict)
