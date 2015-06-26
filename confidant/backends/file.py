from contextlib import contextmanager
import json

from confidant.backends import BaseBackend, BackendNotInitializedError

__author__ = 'gautam'


class FileBackend(BaseBackend):
    """
    Not for use in production, This is merely for local testing
    """

    def __init__(self, file_path):
        """

        :param file_path: The path to the file
        :return:
        """
        super(FileBackend, self).__init__()
        self.file_path = file_path

    @contextmanager
    def __get_file(self, mode='r'):
        with open(self.file_path, mode) as fp:
            yield fp

    def initialize(self):
        """
        Writes an empty json to the file
        :return:
        """
        with self.__get_file('w') as fp:
            fp.write('{}')

    def get(self, key):
        try:
            with self.__get_file() as fp:
                data = json.load(fp)
                return data.get(key)
        except ValueError as e:
            raise BackendNotInitializedError("Unable to decode file, Try calling the initialize method", e)

    def export_data(self):
        with self.__get_file() as fp:
            return json.load(fp)

    def set(self, key, value):
        try:
            with self.__get_file('r') as fp:
                data_dict = json.load(fp)
        except ValueError as e:
            raise BackendNotInitializedError("Unable to decode file, Try calling the initialize method", e)
        data_dict[key] = value
        with self.__get_file('w') as fp:
            json.dump(data_dict, fp)

    def import_data(self, data_dict):
        with self.__get_file('w') as fp:
            json.dump(data_dict, fp)
