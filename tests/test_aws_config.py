import os
import subprocess
import unittest

from confidant import aws_config

__author__ = 'gautam'


class TestAWSConfig(unittest.TestCase):
    def test_get_aws_config_does_not_exist(self):
        dot_aws = os.path.join(os.path.expanduser("~"), '.aws')
        credentials = os.path.join(dot_aws, 'credentials')
        credentials_backup = os.path.join(dot_aws, 'credentials.backup')
        if os.path.exists(credentials):
            subprocess.check_output(['cp', credentials, credentials_backup])
            os.remove(credentials)
        with self.assertRaises(aws_config.AWSConfigNotFound) as ctx:
            aws_config.get_aws_config()

        if os.path.exists(credentials_backup):
            subprocess.check_output(['mv', credentials_backup, credentials])