# confidant
Simple configuration management 

<a href="https://travis-ci.org/gautamk/confidant">
![](https://img.shields.io/travis/gautamk/confidant.svg)
</a>

<a href="https://pypi.python.org/pypi/confidant">
![](https://img.shields.io/pypi/v/confidant.svg)
</a>


* Free software: MIT license

# Installation

```
pip install confidant
```

# Choose a Backend

confidant supports the following backends 

- [DynamodbBackend](https://aws.amazon.com/dynamodb/)
- FileBackend (for local testing)

## TODO

- etcd
- redis
- consul
- zookeeper

# Usage

```python
    # In settings.py
    from confidant.backends.dynamodb import DynamodbBackend
    config_backend = DynamodbBackend(table_name='dynamodb_table_name', env='production')

    DB_USER = config_backend.DB_USER
    DB_PASSWORD = config_backend.DB_PASSWORD
```

# Development

Install dependencies

- `pip install -r requirements.txt`
