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
    parser = configparser.ConfigParser()
    parser.read(cfg)
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv['{0}.{1}'.format(section, key)] = value
    return rv


@with_plugins(
    ep for ep in list(iter_entry_points('mapboxcli.mapboxcli_commands')))
@click.group()
@click.version_option(version=mapboxcli.__version__, message='%(version)s')
@cligj.verbose_opt
@cligj.quiet_opt
@click.option('--access-token', help="Your Mapbox access token.")
@click.option(
    '--config', '-c', type=click.Path(exists=True,
    resolve_path=True),
    help="Config file (default: '{0}/mapbox.ini'".format(click.get_app_dir('mapbox')))
@click.pass_context
def main_group(ctx, verbose, quiet, access_token, config):
    """This is the command line interface to Mapbox web services.

    Mapbox web services require an access token. Your token is shown
    on the https://www.mapbox.com/studio/account/tokens/ page when you are
    logged in. The token can be provided on the command line

      $ mapbox --access-token MY_TOKEN ...

    as an environment variable named MAPBOX_ACCESS_TOKEN (higher
    precedence) or MapboxAccessToken (lower precedence).

    \b
      $ export MAPBOX_ACCESS_TOKEN=MY_TOKEN
      $ mapbox ...

    or in a config file

    \b
      ; configuration file mapbox.ini
      [mapbox]
      access-token = MY_TOKEN

    The OS-dependent default config file path is something like

    \b
      ~/Library/Application Support/mapbox/mapbox.ini
      ~/.config/mapbox/mapbox.ini
      ~/.mapbox/mapbox.ini

    """
    ctx.obj = {}
    config = config or os.path.join(click.get_app_dir('mapbox'), 'mapbox.ini')
    cfg = read_config(config)
    if cfg:
        ctx.obj['config_file'] = config
    ctx.obj['cfg'] = cfg
    ctx.default_map = cfg

    verbosity = (os.environ.get('MAPBOX_VERBOSE') or
                 ctx.lookup_default('mapbox.verbosity') or 0)
    if verbose or quiet:
        verbosity = verbose - quiet
    verbosity = int(verbosity)
    configure_logging(verbosity)

    access_token = (access_token or os.environ.get('MAPBOX_ACCESS_TOKEN') or
                    os.environ.get('MapboxAccessToken') or
                    ctx.lookup_default('mapbox.access-token'))

    ctx.obj['verbosity'] = verbosity
    ctx.obj['access_token'] = access_token
