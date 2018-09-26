import json

import click

import mapbox

from mapboxcli.errors import MapboxCLIException


@click.command(
    short_help="Returns data about specific features from vector tilesets"
)

@click.argument(
    "map_id",
    nargs=-1,
    required=True
)

@click.argument(
    "lon",
     nargs=1,
     required=True
)

@click.argument(
    "lat",
    nargs=1,
    required=True
)

@click.option(
    "--radius",
    "-r",
    type=click.IntRange(0, ),
    help="The approximate distance in meters to query"
)

@click.option(
    "--limit",
    "-l",
    type=click.IntRange(1, 50),
    help="The number of features to return"
)

@click.option(
    "--dedupe/--no-dedupe",
    default=True,
    help="Whether to remove duplicate results"
)

@click.option(
    "--geometry",
    "-g",
    type=click.Choice(mapbox.Tilequery.valid_geometries),
    help="The geometry type to query"
)

@click.option(
    "--layer",
    "-y",
    multiple=True,
    help="The layer to query"
)

@click.option(
    "--output",
    "-o",
    type=click.File("w"),
    help="Whether to save the results to a file"
)

@click.pass_context
def tilequery(ctx, map_id, lon, lat, radius, 
              limit, dedupe, geometry, layer, output):
    """Returns data about specific features from vector tilesets.

         $ mapbox tilequery <map_id> <lon> <lat>

         $ mapbox tilequery mapbox.mapbox-streets-v10 0.0 1.1


         Note: Preface negative longitude or latitude arguments with --.

         $ mapbox tilequery <map_id> -- <-lon> <lat>

         $ mapbox tilequery mapbox.mapbox-streets-v10 -- -0.0 1.1


         $ mapbox tilequery <map_id> <lon> -- <-lat>

         $ mapbox tilequery mapbox.mapbox-streets-v10 0.0 -- -1.1

       An access token is required.  See "mapbox --help".
    """

    access_token = (ctx.obj and ctx.obj.get("access_token")) or None

    service = mapbox.Tilequery(access_token=access_token)

    try:
        res = service.tilequery(
            list(map_id),
            lon=float(lon),
            lat=float(lat),
            radius=radius,
            limit=limit,
            dedupe=dedupe,
            geometry=geometry,
            layers=list(layer) if layer else None,
        )
    except mapbox.errors.ValidationError as exc:
        raise click.BadParameter(str(exc))

    if res.status_code == 200:
        if output:
            output.write(json.dumps(res.geojson()))
        else:
            click.echo(json.dumps(res.geojson()))
    else:
        raise MapboxCLIException(res.text.strip())
