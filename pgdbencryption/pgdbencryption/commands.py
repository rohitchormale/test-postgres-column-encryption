"""
This module implements flask-cli commands.

@author: Rohit Chormale
"""


import click
from flask.cli import AppGroup

pgdbencryption_cli = AppGroup("pgdbencryption")


"""
Example command

@pgdbencryption_cli.command("add-user")
@click.option("--arg1")
@click.option("--arg2")
@click.option("--arg3")
def add_user(arg1, arg2, arg3):
    print("Command executed successfully")
"""
