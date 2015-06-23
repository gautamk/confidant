import importlib
import json
import logging
from decimal import Decimal

__author__ = 'gautam'

import click

SUPPORTED_BACKENDS = ['dynamodb']


@click.command()
@click.argument('backend_name', type=click.Choice(SUPPORTED_BACKENDS))
@click.argument('table_name')
def init(backend_name, table_name):
    backend_module = importlib.import_module('confidant.backends.' + backend_name)
    logging.debug('init backend_class ' + str(backend_module))
    backend = backend_module.init(table_name)
    backend.init()


@click.command()
@click.argument('backend_name', type=click.Choice(SUPPORTED_BACKENDS))
@click.argument('table_name')
@click.argument('environment')
@click.argument('json_file', type=click.File('rb'))
def import_json(backend_name, table_name, environment, json_file):
    backend_module = importlib.import_module('confidant.backends.' + backend_name)
    logging.debug('init backend_class ' + str(backend_module))
    backend = backend_module.init(table_name)
    json_data = json.load(json_file)
    backend.import_data(environment, json_data)


@click.command()
@click.argument('backend_name', type=click.Choice(SUPPORTED_BACKENDS))
@click.argument('table_name')
@click.argument('environment')
@click.argument('json_file', type=click.File('w'))
def export_json(backend_name, table_name, environment, json_file):
    backend_module = importlib.import_module('confidant.backends.' + backend_name)
    logging.debug('init backend_class ' + str(backend_module))
    backend = backend_module.init(table_name)
    data_dict = backend.export_data(environment)
    json.dump(data_dict, json_file, indent=2, default=lambda o: int(o) if isinstance(o, Decimal) else str(o))


@click.group(invoke_without_command=True)
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    if ctx.invoked_subcommand is None:
        click.echo("use confidant --help to get more info")
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)


map(cli.add_command, [init, import_json, export_json])

if __name__ == '__main__':
    cli()
