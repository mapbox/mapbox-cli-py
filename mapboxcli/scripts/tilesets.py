import json

import click
import cligj

import mapbox
from mapboxcli.errors import MapboxCLIException

@click.command(
    short_help="List all tilesets for an account"
)

@click.option(
    "--tileset-type",
    "-t",
    type=click.Choice(mapbox.Tilesets.valid_tileset_types),
    help="Filter results by type"
)

@click.option(
    "--visibility",
    "-v",
    type=click.Choice(mapbox.Tilesets.valid_visibilities),
    help="Filter results by visibility"
)

@click.option(
    "--sortby",
    "-s",
    type=click.Choice(mapbox.Tilesets.valid_sortbys),
    help="Sort results by timestamp"
)

@click.option(
    "--limit",
    "-l",
    help="Limit number of results (pagination)"
)

@click.pass_context
def tilesets(ctx, tileset_type, visibility, sortby, limit):
    """The Mapbox Tilesets API supports reading
    metadata for raster and vector tilesets.

    mapbox tilesets 

    An access token is required.  See "mapbox --help".
    """

    access_token = (ctx.obj and ctx.obj.get("access_token")) or None

    service = mapbox.Tilesets(access_token=access_token)

    try:
        res = service.tilesets(
            tileset_type=tileset_type,
            visibility=visibility,
            sortby=sortby,
            limit=int(limit) if limit is not None else None
        )
    except mapbox.errors.ValidationError as exc:
        raise click.BadParameter(str(exc))

    if res.status_code == 200:
        click.echo(json.dumps(res.json()))
    else:
        raise MapboxCLIException(res.text.strip())
