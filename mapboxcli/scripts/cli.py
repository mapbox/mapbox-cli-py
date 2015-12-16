"""
Main click group for CLI
"""

import logging
import os
import sys

import click
from click_plugins import with_plugins
import cligj
from pkg_resources import iter_entry_points

import mapboxcli
from mapboxcli.compat import configparser


def configure_logging(verbosity):
    log_level = max(10, 30 - 10*verbosity)
    logging.basicConfig(stream=sys.stderr, level=log_level)


def read_config(cfg):
    parser = configparser.RawConfigParser()
    parser.read([cfg])
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv['%s.%s' % (section, key)] = value
    return rv


@with_plugins(
    ep for ep in list(iter_entry_points('mapboxcli.mapboxcli_commands')))
@click.group()
@click.version_option(version=mapboxcli.__version__, message='%(version)s')
@cligj.verbose_opt
@cligj.quiet_opt
@click.option('--access-token', envvar='MAPBOX_ACCESS_TOKEN',
              help="Your Mapbox access token.")
@click.option('--config', '-c', type=click.Path(),
              default=os.path.join(click.get_app_dir('mapbox'), 'mapbox.ini'),
              help="Config file")
@click.pass_context
def main_group(ctx, verbose, quiet, access_token, config):
    """This is the command line interface to Mapbox web services.

    Mapbox web services require an access token. Your token is shown
    on the https://www.mapbox.com/developers/api/ page when you are
    logged in. The token can be provided on the command line

      $ mapbox --access-token MY_TOKEN ...

    or as an environment variable named MAPBOX_ACCESS_TOKEN or
    MapboxAccessToken.

    \b
      $ export MAPBOX_ACCESS_TOKEN=MY_TOKEN
      $ mapbox ...

    """
    cfg = read_config(config)
    if verbose or quiet:
        verbosity = verbose - quiet
    else:
        verbosity = int(cfg.get('mapbox.verbosity', 0))
    access_token = access_token or cfg.get('mapbox.access-token')
    configure_logging(verbosity)
    ctx.obj = {}
    ctx.obj['verbosity'] = verbosity
    ctx.obj['access_token'] = access_token
