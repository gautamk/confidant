import random
import string
import unittest

__author__ = 'gautam'


class BaseTest(unittest.TestCase):
    def random_string(self):
        max_len = random.randint(3, 100)
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(max_len))

    def random_dict(self):
        max_len = random.randint(1, 100)
        return {self.random_string(): self.random_string() for _ in range(max_len)}
