import json
import logging
import re

import click
import mapbox

from mbx.compat import map


@click.command(short_help="Surface profiles from vector tiles")
@click.argument('mapid', required=True)
@click.argument('layer', required=True)
@click.argument('fields', required=True)
@click.argument('waypoints', default='-', nargs=-1, required=True)
@click.option('--zoom', '-z', type=int, default=14,
              help="Zoom level to query (default: 14)")
@click.option('--interpolate/--no-interpolate', default=True,
              help="Weighted average interpolation (default: True)")
@click.option('--geojson/--no-geojson', default=False,
              help="Return geojson feature collection (default: full response json)")
@click.option('--output', '-o', default='-',
              help="Save output to a file.")
@click.pass_context
def surface(ctx, waypoints, geojson, profile, alternatives,
               instructions, geometry, steps, output):
    """Mapbox Surface API enables flexible querying of data stored in
vector tiles on Mapbox, to create results like elevation profiles.

      $ mbx surface mapbox.mapbox-terrain-v1 contour ele \\
\b
            "[-122.681, 45.528]" "[-122.716, 45.525]"

An access token is required, see `mbx --help`.
    """
    pass

