from itertools import chain
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

    for flike in features_like:
        try:
            # It's a file/stream with GeoJSON
            src = iter(click.open_file(flike, mode='r'))
            for feature in iter_features(src):
                features.append(feature)
        except IOError:
            # It's a coordinate string
            coords = list(coords_from_query(flike))
            feature = {
                'type': 'Feature',
                'properties': {},
                'geometry': {
                    'type': 'Point',
                    'coordinates': coords}}
            features.append(feature)

    return features


def iter_features(src):
    """Yield features from a src that may be either a GeoJSON feature
    text sequence or GeoJSON feature collection."""
    first_line = next(src)
    # If input is RS-delimited JSON sequence.
    if first_line.startswith(u'\x1e'):
        buffer = first_line.strip(u'\x1e')
        for line in src:
            if line.startswith(u'\x1e'):
                if buffer:
                    feat = json.loads(buffer)
                    yield feat
                buffer = line.strip(u'\x1e')
            else:
                buffer += line
        else:
            feat = json.loads(buffer)
            yield feat
    else:
        try:
            feat = json.loads(first_line)
            assert feat['type'] == 'Feature'
            yield feat
            for line in src:
                feat = json.loads(line)
                yield feat
        except (KeyError, AssertionError, ValueError):
            text = "".join(chain([first_line], src))
            for feat in json.loads(text)['features']:
                yield feat

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
