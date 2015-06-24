import unittest

from boto.dynamodb2.layer1 import DynamoDBConnection

from confidant.backends.dynamodb import DynamodbBackend

__author__ = 'gautam'


class TestDaynamodbBackend(unittest.TestCase):
    def setUp(self):
        super(TestDaynamodbBackend, self).setUp()
        self.conn = DynamoDBConnection(
            host='localhost',
            port=8000,
            aws_access_key_id='anything',
            aws_secret_access_key='anything',
            is_secure=False)
        self.backend = DynamodbBackend('testtable', 'prd')

    def test_initialize(self):
        self.backend.initialize()

