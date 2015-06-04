import os
import unittest

__author__ = 'gautam'
from confidant.backends import dynamodb


class TestDyanmodbBackend(unittest.TestCase):
    def setUp(self):
        self.renderer = dynamodb.BackendRenderer(os.environ.get('TABLE_NAME'))

    def test_get_key(self):
        self.renderer.get('')
