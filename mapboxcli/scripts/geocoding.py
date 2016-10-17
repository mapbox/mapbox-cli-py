import logging
from itertools import chain
import json
import re

import click
import mapbox

from mapboxcli.compat import map
from mapboxcli.errors import MapboxCLIException


def iter_query(query):
    """Accept a filename, stream, or string.
    Returns an iterator over lines of the query."""
    try:
        itr = click.open_file(query).readlines()
    except IOError:
        itr = [query]
    return itr


def coords_from_query(query):
    """Transform a query line into a (lng, lat) pair of coordinates."""
    try:
        coords = json.loads(query)
    except ValueError:
        vals = re.split(r'[,\s]+', query.strip())
        coords = [float(v) for v in vals]
    return tuple(coords[:2])


def echo_headers(headers, file=None):
    """Echo headers, sorted."""
    for k, v in sorted(headers.items()):
        click.echo("{0}: {1}".format(k.title(), v), file=file)
    click.echo(file=file)


@click.command(short_help="Geocode an address or coordinates.")
@click.argument('query', default='-', required=False)
@click.option(
    '--forward/--reverse',
    default=True,
    help="Perform a forward or reverse geocode. [default: forward]")
@click.option('--include', '-i', 'include_headers',
              is_flag=True, default=False,
              help="Include HTTP headers in the output.")
@click.option(
    '--lat', type=float, default=None,
    help="Bias results toward this latitude (decimal degrees). --lon "
         "is also required.")
@click.option(
    '--lon', type=float, default=None,
    help="Bias results toward this longitude (decimal degrees). --lat "
         "is also required.")
@click.option(
    '--place-type', '-t', multiple=True, metavar='NAME', default=None,
    type=click.Choice(mapbox.Geocoder().place_types.keys()),
    help="Restrict results to one or more place types.")
@click.option('--output', '-o', default='-', help="Save output to a file.")
@click.option('--dataset', '-d', default='mapbox.places',
              type=click.Choice(("mapbox.places", "mapbox.places-permanent")),
              help="Source dataset for geocoding, [default: mapbox.places]")
@click.option('--country', default=None,
              help="Restrict forward geocoding to specified country codes,"
                   "comma-separated")
@click.option('--bbox', default=None,
              help="Restrict forward geocoding to specified bounding box,"
                   "given in minX,minY,maxX,maxY coordinates.")
@click.option('--features', is_flag=True, default=False,
              help="Return results as line-delimited GeoJSON Feature sequence, "
                   "not a FeatureCollection")
@click.option('--limit', type=int, default=None,
              help="Limit the number of returned features")
@click.pass_context
def geocoding(ctx, query, forward, include_headers, lat, lon,
              place_type, output, dataset, country, bbox, features, limit):
    """This command returns places matching an address (forward mode) or
    places matching coordinates (reverse mode).

    In forward (the default) mode the query argument shall be an address
    such as '1600 pennsylvania ave nw'.

      $ mapbox geocoding '1600 pennsylvania ave nw'

    In reverse mode the query argument shall be a JSON encoded array
    of longitude and latitude (in that order) in decimal degrees.

      $ mapbox geocoding --reverse '[-77.4371, 37.5227]'

    An access token is required, see `mapbox --help`.
    """
    verbosity = (ctx.obj and ctx.obj.get('verbosity')) or 2
    logger = logging.getLogger('mapbox')

    access_token = (ctx.obj and ctx.obj.get('access_token')) or None
    stdout = click.open_file(output, 'w')

    geocoder = mapbox.Geocoder(name=dataset, access_token=access_token)

    if forward:
        if country:
            country = [x.lower() for x in country.split(",")]

        if bbox:
            try:
                bbox = tuple(map(float, bbox.split(',')))
            except ValueError:
                bbox = json.loads(bbox)

        for q in iter_query(query):
            try:
                resp = geocoder.forward(
                    q, types=place_type, lat=lat, lon=lon,
                    country=country, bbox=bbox, limit=limit)
            except mapbox.errors.ValidationError as exc:
                raise click.BadParameter(str(exc))

            if include_headers:
                echo_headers(resp.headers, file=stdout)
            if resp.status_code == 200:
                if features:
                    collection = json.loads(resp.text)
                    for feat in collection['features']:
                        click.echo(json.dumps(feat), file=stdout)
                else:
                    click.echo(resp.text, file=stdout)
            else:
                raise MapboxCLIException(resp.text.strip())
    else:
        for lon, lat in map(coords_from_query, iter_query(query)):
            try:
                resp = geocoder.reverse(
                    lon=lon, lat=lat, types=place_type, limit=limit)
            except mapbox.errors.ValidationError as exc:
                raise click.BadParameter(str(exc))

            if include_headers:
                echo_headers(resp.headers, file=stdout)
            if resp.status_code == 200:
                if features:
                    collection = json.loads(resp.text)
                    for feat in collection['features']:
                        click.echo(json.dumps(feat), file=stdout)
                else:
                    click.echo(resp.text, file=stdout)
            else:
                raise MapboxCLIException(resp.text.strip())
