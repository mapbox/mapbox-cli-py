import click

import mapbox
from .helpers import MapboxCLIException

@click.command(short_help="Upload datasets to Mapbox accounts")
@click.argument('tileset', required=True)
@click.argument('infile', required=True)
@click.option('--name', default=None, help="Name for the data upload")
@click.pass_context
def upload(ctx, tileset, infile, name):
    """Upload data to Mapbox accounts.
    All endpoints require authentication.
    Uploaded data lands at https://www.mapbox.com/data/
    and can be used in new or existing projects.

      $ x-mapbox upload username.data data.geojson

    Note that the tileset must start with your username.
    An access token with upload scope is required, see `x-mapbox --help`.
    """
    stdout = click.open_file('-', 'w')
    access_token = (ctx.obj and ctx.obj.get('access_token')) or None

    try:
        username, _ = tileset.split(".")
    except ValueError:
        raise MapboxCLIException("tileset must be of the form "
                                 "<username>.<dataname>")

    service = mapbox.Uploader(username, access_token=access_token)
    try:
        res = service.upload(infile, tileset, name)
    except KeyError as exc:  # TODO better exception from python SDK
        if exc.message == 'accessKeyId':
            raise MapboxCLIException(
                "An access token with upload scope is required")
        else:
            raise exc
        import ipdb; ipdb.set_trace()

    if res.status_code == 201 :
        click.echo(res.text, file=stdout)
    else:
        raise MapboxCLIException(res.text.strip())
