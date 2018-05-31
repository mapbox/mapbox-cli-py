import json

import click
import cligj
import mapbox

from mapboxcli.errors import MapboxCLIException


@click.command(short_help="Routing between waypoints.")
@cligj.features_in_arg
@click.option('--profile', default="mapbox.driving",
              type=click.Choice(mapbox.Directions().valid_profiles),
              help="Mapbox direction profile id")
@click.option('--alternatives/--no-alternatives', default=True,
              help="Generate alternative routes?")
@click.option('--instructions', default="text",
              type=click.Choice(mapbox.Directions().valid_instruction_formats),
              help="Format for route instructions")
@click.option('--geometry', default="geojson",
              type=click.Choice(mapbox.Directions().valid_geom_encoding),
              help="Geometry encoding")
@click.option('--steps/--no-steps', default=True,
              help="Include steps in the response")
@click.option('--geojson/--no-geojson', default=False,
              help="Return geojson feature collection (default: full response json)")
@click.option('--output', '-o', default='-',
              help="Save output to a file.")
@click.pass_context
def directions(ctx, features, geojson, profile, alternatives,
               instructions, geometry, steps, output):
    """Calculate optimal route with turn-by-turn directions
    between up to 25 waypoints.

      $ mapbox directions "[-122.681032, 45.528334]" "[-122.71679, 45.525135]"

    An access token is required, see `mapbox --help`.
    """
    stdout = click.open_file(output, 'w')
    access_token = (ctx.obj and ctx.obj.get('access_token')) or None
    if geojson:
        geometry = 'geojson'

    service = mapbox.Directions(access_token=access_token)

    try:
        res = service.directions(
            features,
            steps=steps,
            alternatives=alternatives,
            instructions=instructions,
            geometry=geometry,
            profile=profile)
    except mapbox.errors.ValidationError as exc:
        raise click.BadParameter(str(exc))

    if res.status_code == 200:
        if geojson:
            click.echo(json.dumps(res.geojson()), file=stdout)
        else:
            click.echo(res.text, file=stdout)
    else:
        raise MapboxCLIException(res.text.strip())
