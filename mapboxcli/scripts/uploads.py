import click

import mapbox
from mapboxcli.errors import MapboxCLIException


@click.command(short_help="Upload datasets to Mapbox accounts")
@click.argument('tileset', required=True)
@click.argument('infile', type=click.File('r'), required=False)
@click.option('--name', default=None, help="Name for the data upload")
@click.pass_context
def upload(ctx, tileset, infile, name):
    """Upload data to Mapbox accounts.
    All endpoints require authentication.
    Uploaded data lands at https://www.mapbox.com/data/
    and can be used in new or existing projects.

      $ mapbox upload username.data data.geojson

    Note that the tileset must start with your username.
    An access token with upload scope is required, see `mapbox --help`.
    """
    access_token = (ctx.obj and ctx.obj.get('access_token')) or None

    service = mapbox.Uploader(access_token=access_token)

    try:
        res = service.upload(infile, tileset, name)
    except (mapbox.errors.ValidationError, IOError) as exc:
        raise click.BadParameter(str(exc))

    if res.status_code == 201:
        click.echo(res.text)
    else:
        raise MapboxCLIException(res.text.strip())
