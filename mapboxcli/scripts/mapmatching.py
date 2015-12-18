import click
import cligj

import mapbox
from mapboxcli.errors import MapboxCLIException

@click.command('mapmatching', short_help="Snap GPS traces to OpenStreetMap")
@cligj.features_in_arg
@click.option("--gps-precision", default=4, type=int,
              help="Assumed precision of tracking device (default 4 meters)")
@click.option('--profile', default="mapbox.driving",
              type=click.Choice(mapbox.MapMatcher().valid_profiles),
              help="Mapbox profile id")
@click.pass_context
def match(ctx, features, profile, gps_precision):
    """Mapbox Map Matching API lets you use snap your GPS traces
to the OpenStreetMap road and path network.

      $ mapbox mapmatching trace.geojson

An access token is required, see `mapbox --help`.
    """
    access_token = (ctx.obj and ctx.obj.get('access_token')) or None

    features = list(features)
    if len(features) != 1:
        raise click.BadParameter(
            "Mapmatching requires a single LineString feature")

    service = mapbox.MapMatcher(access_token=access_token)
    try:
        res = service.match(
            features[0],
            profile=profile,
            gps_precision=gps_precision)
    except mapbox.errors.ValidationError as exc:
        raise click.BadParameter(str(exc))

    if res.status_code == 200:
        stdout = click.open_file('-', 'w')
        click.echo(res.text, file=stdout)
    else:
        raise MapboxCLIException(res.text.strip())
