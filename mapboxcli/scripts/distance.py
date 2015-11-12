import json
import logging
import re

import click
import mapbox

from mbx.compat import map


@click.command(short_help="Distance matrix of travel times between waypoints.")
@click.argument('waypoints', default='-', nargs=-1, required=True)
@click.option('--profile', default="driving", type=click.Choice([
              'driving', 'walking', 'cycling']),
              help="Mapbox direction profile id")
@click.option('--output', '-o', default='-',
              help="Save output to a file.")
@click.pass_context
def distance(ctx, waypoints, profile, output):
    """The Distance API returns all travel times between
    many points (also known as Distance Matrix). This is often
    used as input for solving routing optimization problems.

      $ mbx distance "[-122.681, 45.528]" "[-122.716, 45.525]"

    The output is a json object with a "durations" key
    containing a 2D array of travel times between waypoints.

    An access token is required, see `mbx --help`.
    """
    pass

