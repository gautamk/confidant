from ConfigParser import SafeConfigParser
import os

__author__ = 'gautam'


class AWSConfigNotFound(EnvironmentError):
    pass


def get_aws_config(section='default'):
    """
    Fetches the aws credentials from ~/.aws/credentials
    :return: tuple(aws_access_key_id, aws_secret_access_key)
    """
    dot_aws = os.path.join(os.path.expanduser("~"), '.aws')
    credentials = os.path.join(dot_aws, 'credentials')
    if not os.path.isfile(credentials):
        raise AWSConfigNotFound()
    config = SafeConfigParser()
    config.read(credentials)
    aws_access_key_id = config.get(section, 'aws_access_key_id')
    aws_secret_access_key = config.get(section, 'aws_secret_access_key')
    return aws_access_key_id, aws_secret_access_key


def put_aws_config(aws_access_key_id, aws_secret_access_key, section='default'):
    dot_aws = os.path.join(os.path.expanduser("~"), '.aws')
    credentials = os.path.join(dot_aws, 'credentials')
    config = SafeConfigParser()
    config.add_section(section)
    config.set(section, 'aws_access_key_id', aws_access_key_id)
    config.set(section, 'aws_secret_access_key', aws_secret_access_key)
    with open(credentials, 'w') as f:
        config.write(f)