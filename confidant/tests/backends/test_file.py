import json
import os
import tempfile

from confidant.backends import BackendNotInitializedError
from confidant.backends.file import FileBackend
from confidant.tests import BaseTest

__author__ = 'gautam'


class TestFileBackend(BaseTest):
    def setUp(self):
        super(TestFileBackend, self).setUp()
        _, self.file_path = tempfile.mkstemp()
        self.backend = FileBackend(self.file_path)

    def tearDown(self):
        os.remove(self.file_path)

    def test_initialize(self):
        self.backend.initialize()
        with open(self.file_path) as fp:
            self.assertEqual(fp.read(), '{}')

    def test_get(self):
        key, value = self.random_string(), self.random_string()
        with open(self.file_path, 'w') as fp:
            json.dump({key: value}, fp)
        self.assertEqual(self.backend.get(key), value)

    def test_set(self):
        self.backend.initialize()
        key, value = self.random_string(), self.random_string()
        self.backend.set(key, value)
        with open(self.file_path, 'r') as fp:
            data = json.load(fp)
            self.assertEqual(data[key], value)

    def test_get_uninitialized(self):
        with self.assertRaises(BackendNotInitializedError):
            self.backend.get('')

    def test_set_uninitialized(self):
        with self.assertRaises(BackendNotInitializedError):
            self.backend.set(
                key=self.random_string(),
                value=self.random_string())

    def test_import_data(self):
        random_dict = self.random_dict()
        self.backend.import_data(random_dict)
        with open(self.file_path) as fp:
            self.assertDictEqual(json.load(fp), random_dict)

    def test_export_data(self):
        random_dict = self.random_dict()
        with open(self.file_path, 'w') as fp:
            json.dump(random_dict, fp)
        self.assertDictEqual(self.backend.export_data(), random_dict)
