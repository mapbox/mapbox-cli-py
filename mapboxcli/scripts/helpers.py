import json

import click

def normalize_waypoints(waypoints):
    point_features = []
    if len(waypoints) == 0:
        waypoints = ('-',)
    for wp in waypoints:
        try:
            stdin = click.open_file(wp, 'r')
            waypt = json.loads(stdin.read())
        except IOError:
            waypt = {
                'type': 'Feature',
                'properties': {},
                'geometry': {
                    'type': 'Point',
                    'coordinates': json.loads(wp)}}

        if waypt['type'] == 'Feature' and waypt['geometry']['type'] == "Point":
            point_features.append(waypt)
        elif waypt['type'] == 'FeatureCollection':
            for feature in waypt['features']:
                if feature['geometry']['type'] == "Point":
                    point_features.append(feature)
                else:
                    pass  # TODO
        else:
            pass  # TODO

    return point_features


class MapboxCLIException(click.ClickException):
    pass
