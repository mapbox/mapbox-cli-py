from io import BytesIO
import os
import sys

import click

import mapbox
from mapboxcli.errors import MapboxCLIException


@click.command(short_help="Upload datasets to Mapbox accounts")
@click.argument('tileset', required=True, type=str, metavar='TILESET')
@click.argument('datasource', type=str, default='-', metavar='[SOURCE]')
@click.option('--name', default=None, help="Name for the data upload")
@click.option('--patch', is_flag=True, default=False, help="Enable patch mode")
@click.pass_context
def upload(ctx, tileset, datasource, name, patch):
    """Upload data to Mapbox accounts.

    Uploaded data lands at https://www.mapbox.com/data/ and can be used
    in new or existing projects. All endpoints require authentication.

    You can specify the tileset id and input file

      $ mapbox upload username.data mydata.geojson

    Or specify just the tileset id and take an input file on stdin

      $ cat mydata.geojson | mapbox upload username.data

    The --name option defines the title as it appears in Studio and
    defaults to the last part of the tileset id, e.g. "data"

    Note that the tileset must start with your username. An access
    token with upload scope is required, see `mapbox --help`.

    Your account must be flagged in order to use the patch mode
    feature.
    """
    access_token = (ctx.obj and ctx.obj.get('access_token')) or None

    service = mapbox.Uploader(access_token=access_token)

    if name is None:
        name = tileset.split(".")[-1]

    if datasource.startswith('https://'):
        # Skip staging. Note this this only works for specific buckets.
        res = service.create(datasource, tileset, name=name, patch=patch)

    else:
        sourcefile = click.File('rb')(datasource)

        if hasattr(sourcefile, 'name'):
            filelen = (
                1 if sourcefile.name == '<stdin>'
                else os.stat(sourcefile.name).st_size)
        else:
            filelen = (len(sourcefile.getbuffer())
                       if hasattr(sourcefile, 'getbuffer') else 1)

        with click.progressbar(length=filelen, label='Uploading data source',
                               fill_char="#", empty_char='-',
                               file=sys.stderr) as bar:

            def callback(num_bytes):
                """Update the progress bar"""
                bar.update(num_bytes)

            res = service.upload(sourcefile, tileset, name, patch=patch,
                                 callback=callback)

    if res.status_code == 201:
        click.echo(res.text)
    else:
        raise MapboxCLIException(res.text.strip())
