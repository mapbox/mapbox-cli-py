from io import BytesIO
import os
import sys

import click

import mapbox
from mapboxcli.errors import MapboxCLIException


@click.command(short_help="Upload datasets to Mapbox accounts")
@click.argument('args', nargs=-1, required=True, metavar="[INFILE] TILESET")
@click.option('--name', default=None, help="Name for the data upload")
@click.option('--patch', is_flag=True, default=False, help="Patch mode")
@click.pass_context
def upload(ctx, args, name, patch):
    """Upload data to Mapbox accounts.
    All endpoints require authentication.
    Uploaded data lands at https://www.mapbox.com/data/
    and can be used in new or existing projects.

    You can specify the input file and tileset id

      $ mapbox upload mydata.geojson username.data

    Or specify just the tileset id and take an input file on stdin

      $ cat mydata.geojson | mapbox upload username.data

    The --name option defines the title as it appears in Studio
    and defaults to the last part of the tileset id, e.g. "data"

    Note that the tileset must start with your username.
    An access token with upload scope is required, see `mapbox --help`.

    Your account must be flagged in order to use the patch mode feature.
    """
    access_token = (ctx.obj and ctx.obj.get('access_token')) or None

    service = mapbox.Uploader(access_token=access_token)

    if len(args) == 1:
        # Tileset specified, file from stdin
        click.echo("Reading data from stdin (Hit Ctl-C to cancel) ...", err=True)
        initial_bytes = click.File("rb")("-").read()
        filelen = len(initial_bytes)
        infile = BytesIO(initial_bytes)
        tileset = args[0]
    elif len(args) == 2:
        # Infile and Tileset are specified
        try:
            infile = click.File("rb")(args[0])
            filelen = os.stat(infile.name).st_size
        except click.ClickException:
            raise click.UsageError(
                "Could not open file: {0} "
                "(check order of command arguments: INFILE TILESET)".format(args[0]))

        tileset = args[1]
    else:
        raise click.UsageError(
            "Must provide either one argument (TILESET) or two (INFILE TILESET)")

    if name is None:
        name = tileset.split(".")[-1]

    with click.progressbar(length=filelen, label='Staging data',
                           file=sys.stderr) as bar:

        def callback(num_bytes):
            """Update the progress bar"""
            bar.update(num_bytes)

        res = service.upload(infile, tileset, name, patch=patch,
                             callback=callback)

    if res.status_code == 201:
        click.echo(res.text)
    else:
        raise MapboxCLIException(res.text.strip())
