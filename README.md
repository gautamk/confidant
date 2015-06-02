# confidant
Simple configuration management 


# Installation

`pip install confidant`

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
