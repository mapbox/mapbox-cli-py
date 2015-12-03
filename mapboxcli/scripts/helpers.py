import json
import re

import click


class MapboxCLIException(click.ClickException):
    pass


def normalize_waypoints(waypoints):
    point_features = []
    if len(waypoints) == 0:
        waypoints = ('-',)
    for wp in waypoints:
        try:
            # It's a file/stream with GeoJSON
            stdin = click.open_file(wp, 'r')
            waypt = json.loads(stdin.read())
        except IOError:
            # It's a coordinate string
            coords = list(coords_from_query(wp))
            waypt = {
                'type': 'Feature',
                'properties': {},
                'geometry': {
                    'type': 'Point',
                    'coordinates': coords}}

        if waypt['type'] == 'Feature' and waypt['geometry']['type'] == "Point":
            point_features.append(waypt)
        elif waypt['type'] == 'FeatureCollection':
            for feature in waypt['features']:
                point_features.append(feature)
        else:
            pass  # TODO, handle non-feature or non-point feature

    return point_features


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
        vals = re.split(r"\,*\s*", query.strip())
        coords = [float(v) for v in vals]
    return tuple(coords[:2])


def echo_headers(headers, file=None):
    """Echo headers, sorted."""
    for k, v in sorted(headers.items()):
        click.echo("{0}: {1}".format(k.title(), v), file=file)
    click.echo(file=file)
