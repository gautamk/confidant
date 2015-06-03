# -*- coding: utf-8 -*-

import sys

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
        click.echo("AWS config already setup, delete the file ~/.aws/credentials to setup again")
        sys.exit(1)
    except aws_config.AWSConfigNotFound:
        aws_config.put_aws_config(aws_access_key_id=aws_access_key,
                                  aws_secret_access_key=aws_secret_key)


@click.group()
def cli():
    """
    Docs
    """


cli.add_command(version)
cli.add_command(setup)
