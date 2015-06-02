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

- [dynamodb](https://aws.amazon.com/dynamodb/)

## TODO

- etcd
- redis
- consul
- zookeeper

# Usage 

1. Render a configuration template 

`confidant render --backend dynamodb /path/to/template > /path/to/config-file`


# Development

Install dependencies

- `pip install -r requirements.txt`
