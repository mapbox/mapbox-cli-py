import json

import click

import mapbox

from mapboxcli.errors import MapboxCLIException


# mapbox maps

@click.group(
    short_help="Returns tiles and features"
)

@click.pass_context
def maps(ctx):
    """The Mapbox Maps API supports reading raster tilesets,
       vector tilesets, and Mapbox Editor project features.

       An access token is required.  See "mapbox --help".
    """

    access_token = (ctx.obj and ctx.obj.get("access_token")) or None
    service = mapbox.Maps(access_token=access_token)
    ctx.obj["service"] = service


# mapbox maps tile

@maps.command(
    short_help="Returns a tile in the specified format"
)

@click.argument(
    "map_id",
    required=True
)

@click.argument(
    "output",
    type=click.File("wb"),
    required=True
)

@click.option(
    "--column",
    "-x",
    required=True,
    help="The tile's column (x)"
)

@click.option(
    "--row",
    "-y",
    required=True,
    help="The tile's row (y)"
)

@click.option(
    "--zoom-level",
    "-z",
    required=True,
    help="The tile's zoom level (z)"
)

@click.option(
    "--retina/--no-retina",
    default=False,
    help="Whether to return the tile in Retina scale"
)

@click.option(
    "--file-format",
    "-f",
    type=click.Choice(mapbox.Maps.valid_file_formats),
    default="png",
    help="The tile's file format"
)

@click.option(
    "--style-id",
    "-s",
    help="The style id"
)

@click.option(
    "--timestamp",
    "-t",
    help="The style id's ISO-formatted date string"
)

@click.pass_context
def tile(ctx, map_id, output, column, row, 
         zoom_level, retina, file_format, style_id, 
         timestamp): 
    """Returns an image tile, vector tile, or UTFGrid
       in the specified file format.

       mapbox maps tile --column <column> --row <row> --zoom--level <zoom_level> <map_id> <output>

       mapbox maps tile --column 0 --row 0 --zoom 0 mapbox.streets tile.png

       An access token is required.  See "mapbox --help".
    """

    access_token = (ctx.obj and ctx.obj.get("access_token")) or None

    service = ctx.obj.get("service")

    try:
        res = service.tile(
            map_id,
            int(column),
            int(row),
            int(zoom_level),
            retina=retina,
            file_format=file_format,
            style_id=style_id,
            timestamp=timestamp
        )
    except mapbox.errors.ValidationError as exc:
        raise click.BadParameter(str(exc))

    if res.status_code == 200:
        output.write(res.content)
    else:
        raise MapboxCLIException(res.text.strip())


# mapbox maps features

@maps.command(
    short_help="Returns features from Mapbox Editor projects"
)

@click.argument(
    "map_id",
    required=True
)

@click.argument(
    "output",
    type=click.File("w"),
    required=False
)

@click.option(
    "--feature-format",
    "-f",
    type=click.Choice(mapbox.Maps.valid_feature_formats),
    default="json",
    help="The vector's feature format"
)

@click.pass_context
def features(ctx, map_id, output, feature_format):
    """Returns vector features from Mapbox Editor projects 
       as GeoJSON or KML.

       To write output to the console (stdout):

       mapbox maps features <map_id>

       mapbox maps features mapbox.streets

       To write output to a file:

       mapbox maps features <map_id> <output>

       mapbox maps features mapbox.streets features.json

       An access token is required.  See "mapbox --help".
    """

    access_token = (ctx.obj and ctx.obj.get("access_token")) or None

    service = ctx.obj.get("service")

    res = service.features(
        map_id,
        feature_format=feature_format,
    )
    
    if res.status_code == 200:
        if output and feature_format == "json":
           output.write(json.dumps(res.json()))

        if output and feature_format == "kml":
           output.write(res.text)

        if not output and feature_format == "json":
           click.echo(json.dumps(res.json()))

        if not output and feature_format == "kml":
           click.echo(res.text)
    else:
        raise MapboxCLIException(res.text.strip())


# mapbox maps metadata

@maps.command(
    short_help="Returns metadata for a tileset"
)

@click.argument(
    "map_id",
    required=True
)

@click.argument(
    "output",
    type=click.File("w"),
    required=False
)

@click.option(
    "--secure/--no-secure",
    default=False,
    help="Whether to return HTTPS endpoints"
)

@click.pass_context
def metadata(ctx, map_id, output, secure):
    """Returns TileJSON metadata for a tileset.

       To write output to the console (stdout):

       mapbox maps metadata <map_id>

       mapbox maps metadata mapbox.streets

       To write output to a file:

       mapbox maps metadata <map_id> <output>

       mapbox maps metadata mapbox.streets metadata.json

       An access token is required.  See "mapbox --help".
    """

    access_token = (ctx.obj and ctx.obj.get("access_token")) or None

    service = ctx.obj.get("service")

    res = service.metadata(
        map_id,
        secure=secure
    )

    if res.status_code == 200:
        if output:
           output.write(json.dumps(res.json()))

        if not output:
           click.echo(json.dumps(res.json()))

    else:
        raise MapboxCLIException(res.text.strip())


# mapbox maps marker

@maps.command(
    short_help="Returns a single marker"
)

@click.argument(
    "output",
    type=click.File("wb"),
    required=True
)

@click.option(
    "--marker-name",
    "-m",
    type=click.Choice(mapbox.Maps.valid_marker_names),
    required=True,
    help="The marker's shape and size"
)

@click.option(
    "--label",
    "-l",
    help="The marker's alphanumeric label"
)

@click.option(
    "--color",
    "-c",
    help="The marker's color"
)

@click.option(
    "--retina/--no-retina",
    default=False,
    help="Whether to return the tile in Retina scale"
)

@click.pass_context
def marker(ctx, output, marker_name, 
           label, color, retina):
    """Returns a single marker image without any
       background map.

       mapbox maps marker --marker-name <marker_name> <output>

       mapbox maps marker --marker-name pin-s pin-s.png

       An access token is required.  See "mapbox --help".
    """

    access_token = (ctx.obj and ctx.obj.get("access_token")) or None

    service = ctx.obj.get("service")

    try:
        res = service.marker(
            marker_name=marker_name,
            label=label,
            color=color,
            retina=retina
        )
    except mapbox.errors.ValidationError as exc:
        raise click.BadParameter(str(exc))

    if res.status_code == 200:
        output.write(res.content)
    else:
        raise MapboxCLIException(res.text.strip())
