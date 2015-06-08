import importlib
import logging

__author__ = 'gautam'

import click


@click.command()
@click.option("backend", type=click.Choice(['dynamodb']))
@click.option("table_name")
def init(backend, table_name):
    BackendClass = importlib.import_module('confidant.backends.' + backend)
    BackendClass(table_name)


@click.group(invoke_without_command=True)
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    if ctx.invoked_subcommand is None:
        click.echo("use confidant --help to get more info")
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)


map(cli.add_command, [init])
