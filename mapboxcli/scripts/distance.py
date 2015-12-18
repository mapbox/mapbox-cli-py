import click
import cligj

import mapbox
from mapboxcli.errors import MapboxCLIException


@click.command(short_help="Distance matrix of travel times between waypoints.")
@cligj.features_in_arg
@click.option('--profile', default="driving",
              type=click.Choice(mapbox.Distance().valid_profiles),
              help="Mapbox direction profile id")
@click.option('--output', '-o', default='-',
              help="Save output to a file.")
@click.pass_context
def distance(ctx, features, profile, output):
    """The Distance API returns all travel times between
    many points (also known as Distance Matrix). This is often
    used as input for solving routing optimization problems.

      $ mapbox distance "[-122.681, 45.528]" "[-122.716, 45.525]"

    The output is a json object with a "durations" key
    containing a 2D array of travel times between waypoints.

    An access token is required, see `mapbox --help`.
    """
    stdout = click.open_file(output, 'w')
    access_token = (ctx.obj and ctx.obj.get('access_token')) or None
    service = mapbox.Distance(access_token=access_token)

    try:
        res = service.distances(
            features,
            profile=profile)
    except mapbox.errors.ValidationError as exc:
        raise click.BadParameter(str(exc))

    if res.status_code == 200:
        click.echo(res.text, file=stdout)
    else:
        raise MapboxCLIException(res.text.strip())
