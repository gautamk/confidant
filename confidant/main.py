# -*- coding: utf-8 -*-
import logging

import click
import pkg_resources  # part of setuptools

from confidant import aws_config


@click.command()
def version():
    version_number = pkg_resources.require("confidant")[0].version
    click.echo(version_number)


@click.command()
@click.option('--aws-access-key', 'aws_access_key', prompt=True)
@click.option('--aws-secret-key', 'aws_secret_key', prompt=True)
def setup(aws_access_key, aws_secret_key):
    """
    Initial setup to configure confidant
    :return:
    """
    try:
        aws_config.get_aws_config()
        logging.debug("~/.aws/credentials exist")
        raise click.UsageError("AWS config already setup, delete the file ~/.aws/credentials to setup again")
    except aws_config.AWSConfigNotFound:
        aws_config.put_aws_config(aws_access_key_id=aws_access_key,
                                  aws_secret_access_key=aws_secret_key)


@click.command()
@click.argument('backend', type=click.Choice(['dynamodb']))
@click.argument('input', type=click.File('r'))
@click.argument('output', type=click.File('w'))
def render(backend, input, output):
    if backend == 'dynamodb':
        from confidant.backends import dynamodb as module
    else:
        raise click.BadParameter('Backend Not found')
    module.render(input, output)


@click.group(invoke_without_command=True)
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    """
    Docs
    """
    if ctx.invoked_subcommand is None:
        click.echo("use confidant --help to get more info")
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)


map(cli.add_command, [version, setup, render])
