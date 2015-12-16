import os

import click


@click.command(short_help="Show all config settings.")
@click.pass_context
def config(ctx):
    """Show config settings from command line, environment, and config
    files."""
    ctx.default_map = ctx.obj['cfg']

    click.echo("CLI:")
    click.echo("access-token = {0}".format(ctx.obj['access_token']))
    click.echo("verbosity = {0}".format(ctx.obj['verbosity']))
    click.echo("")
    click.echo("Environment:")
    if 'MAPBOX_ACCESS_TOKEN' in os.environ:
        click.echo("MAPBOX_ACCESS_TOKEN = {0}".format(
            os.environ['MAPBOX_ACCESS_TOKEN']))
    elif 'MapboxAccessToken' in os.environ:
        click.echo("MapboxAccessToken = {0}".format(
            os.environ['MapboxAccessToken']))
    click.echo("")
    click.echo("Config file {0}:".format(ctx.obj['config_file']))
    for key, value in ctx.default_map.items():
        click.echo("{0} = {1}".format(key, value))
    click.echo("")
