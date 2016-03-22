from io import BytesIO

import click

import mapbox
from mapboxcli.errors import MapboxCLIException


@click.command(short_help="Upload datasets to Mapbox accounts")
@click.argument('args', nargs=-1, required=True, metavar="[INFILE] TILESET")
@click.option('--name', default=None, help="Name for the data upload")
@click.pass_context
def upload(ctx, args, name):
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
    """
    access_token = (ctx.obj and ctx.obj.get('access_token')) or None

    service = mapbox.Uploader(access_token=access_token)

    if len(args) == 1:
        # Tileset specified, file from stdin
        click.echo("Reading data from stdin (Hit Ctl-C to cancel) ...", err=True)
        infile = BytesIO(click.File("rb")("-").read())
        tileset = args[0]
    elif len(args) == 2:
        # Infile and Tileset are specified
        try:
            infile = click.File("rb")(args[0])
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

    try:
        res = service.upload(infile, tileset, name)
    except (mapbox.errors.ValidationError, IOError) as exc:
        raise click.BadParameter(str(exc))

    if res.status_code == 201:
        click.echo(res.text)
    else:
        raise MapboxCLIException(res.text.strip())
