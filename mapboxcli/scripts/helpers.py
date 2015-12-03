import json
import re

import click


class MapboxCLIException(click.ClickException):
    pass


def normalize_waypoints(waypoints):
    features = normalize_features(waypoints)
    # skip non-points
    return [f for f in features if f['geometry']['type'] == 'Point']


def normalize_features(features_like):
    features = []
    if len(features_like) == 0:
        features_like = ('-',)
    for fl in features_like:
        try:
            # It's a file/stream with GeoJSON
            stdin = click.open_file(fl, 'r')
            geojson_mapping = json.loads(stdin.read())
        except IOError:
            # It's a coordinate string
            coords = list(coords_from_query(fl))
            geojson_mapping = {
                'type': 'Feature',
                'properties': {},
                'geometry': {
                    'type': 'Point',
                    'coordinates': coords}}

        if geojson_mapping['type'] == 'Feature':
            features.append(geojson_mapping)
        elif geojson_mapping['type'] == 'FeatureCollection':
            for feat in geojson_mapping['features']:
                features.append(feat)
        else:
            raise ValueError("Not a valid coordinate, Feature or FeatureCollection")

    return features


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
