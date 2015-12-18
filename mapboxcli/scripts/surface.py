import json

import click
import cligj

import mapbox
from mapboxcli.errors import MapboxCLIException


@click.command(short_help="Surface profiles from vector tiles")
@click.argument('mapid', required=True)
@click.argument('layer', required=True)
@click.argument('fields', required=True)
@cligj.features_in_arg
@click.option('--zoom', '-z', type=int, default=14,
              help="Zoom level to query (default: 14)")
@click.option('--interpolate/--no-interpolate', default=True,
              help="Weighted average interpolation (default: True)")
@click.option('--geojson/--no-geojson', default=True,
              help="Return geojson feature collection (default: True)")
@click.option('--output', '-o', default='-',
              help="Save output to a file.")
@click.pass_context
def surface(ctx, mapid, layer, fields, features,
            zoom, interpolate, geojson, output):
    """Mapbox Surface API enables flexible querying of data stored in
vector tiles on Mapbox, to create results like elevation profiles.

      $ mapbox surface mapbox.mapbox-terrain-v1 contour ele \\
\b
            "[-122.781, 45.528]" "[-122.716, 45.525]"

An access token is required, see `mapbox --help`.
    """
    stdout = click.open_file(output, 'w')
    access_token = (ctx.obj and ctx.obj.get('access_token')) or None
    fields = fields.split(",")

    service = mapbox.Surface(access_token=access_token)

    try:
        res = service.surface(
            features,
            mapid=mapid,
            layer=layer,
            fields=fields,
            geojson=geojson,
            interpolate=interpolate,
            zoom=zoom)
    except mapbox.errors.ValidationError as exc:
        raise click.BadParameter(str(exc))

    if res.status_code == 200:
        if geojson:
            click.echo(json.dumps(res.geojson()), file=stdout)
        else:
            click.echo(res.text, file=stdout)
    else:
        raise MapboxCLIException(res.text.strip())
