import click
import json

import mapbox
from .helpers import MapboxCLIException, normalize_waypoints


@click.command(short_help="Routing between waypoints.")
@click.argument('waypoints', nargs=-1)
@click.option('--profile', default="mapbox.driving", type=click.Choice([
              'mapbox.driving', 'mapbox.walking', 'mapbox.cycling']),
              help="Mapbox direction profile id")
@click.option('--alternatives/--no-alternatives', default=True,
              help="Generate alternative routes?")
@click.option('--instructions', default="text", type=click.Choice(["text", "html"]),
              help="Format for route instructions")
@click.option('--geometry', default="geojson", type=click.Choice([
              'geojson', 'polyline', 'false']), help="Geometry encoding")
@click.option('--steps/--no-steps', default=True,
              help="Include steps in the response")
@click.option('--geojson/--no-geojson', default=False,
              help="Return geojson feature collection (default: full response json)")
@click.option('--output', '-o', default='-',
              help="Save output to a file.")
@click.pass_context
def directions(ctx, waypoints, geojson, profile, alternatives,
               instructions, geometry, steps, output):
    """Calculate optimal route with turn-by-turn directions
    between up to 25 waypoints.

      $ mapbox directions "[-122.681032, 45.528334]" "[-122.71679, 45.525135]"

    An access token is required, see `mapbox --help`.
    """
    stdout = click.open_file(output, 'w')
    access_token = (ctx.obj and ctx.obj.get('access_token')) or None
    point_features = normalize_waypoints(waypoints)
    if geojson:
        geometry = 'geojson'

    service = mapbox.Directions(access_token=access_token)
    res = service.directions(point_features,
                             steps=steps,
                             alternatives=alternatives,
                             instructions=instructions,
                             geometry=geometry,
                             profile=profile)

    if res.status_code == 200:
        if geojson:
            click.echo(json.dumps(res.geojson()), file=stdout)
        else:
            click.echo(res.text, file=stdout)
    else:
        raise MapboxCLIException(res.text.strip())
