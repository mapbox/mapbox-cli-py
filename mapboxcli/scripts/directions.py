import json

import click
import cligj

import mapbox
from mapboxcli.errors import MapboxCLIException


@click.command(short_help="Routing between waypoints")

@cligj.features_in_arg

@click.option(
    "--profile",
    type=click.Choice(mapbox.Directions.valid_profiles),
    default="mapbox/driving",
    help="Routing profile"
)

@click.option(
    "--alternatives/--no-alternatives",
    default=True,
    help="Whether to try to return alternative routes"
)

@click.option(
    "--geometries",
    type=click.Choice(mapbox.Directions.valid_geom_encoding),
    default="geojson",
    help="Format of returned geometry"
)

# Directions.valid_geom_overview contains two items of type str 
# and one item of type bool.  This causes the Directions CLI's 
# --help option to raise a TypeError.  To prevent this, we convert
# the bool to a str.

@click.option(
    "--overview",
    type=click.Choice(str(item) for item in mapbox.Directions.valid_geom_overview),
    help="Type of returned overview geometry"
)

@click.option(
    "--steps/--no-steps",
    default=True,
    help="Whether to return steps and turn-by-turn instructions"
)

@click.option(
    "--continue-straight/--no-continue-straight",
    default=True,
    help="Whether to see the allowed direction of travel when departing the original waypoint"
)

@click.option(
    "--annotations",
    help="Additional metadata along the route" 
)

@click.option(
    "--language",
    help="Language of returned turn-by-turn instructions"
)

@click.option(
    "-o",
    "--output",
    default="-",
    help="Save output to a file"
)

@click.pass_context
def directions(ctx, features, profile, alternatives, 
               geometries, overview, steps, continue_straight, 
               annotations, language, output):
    """The Mapbox Directions API will show you how to get
       where you're going.

       mapbox directions "[0, 0]" "[1, 1]"

       An access token is required.  See "mapbox --help".
    """

    access_token = (ctx.obj and ctx.obj.get("access_token")) or None

    service = mapbox.Directions(access_token=access_token)

    if overview == "False":
        overview = False

    if annotations:
        annotations = annotations.split(",")

    stdout = click.open_file(output, "w")

    try:
        res = service.directions(
            features,
            profile=profile,
            alternatives=alternatives,
            geometries=geometries,
            overview=overview,
            steps=steps,
            continue_straight=continue_straight,
            annotations=annotations,
            language=language
        )
    except mapbox.errors.ValidationError as exc:
        raise click.BadParameter(str(exc))

    if res.status_code == 200:
        if geometries == "geojson":
            click.echo(json.dumps(res.geojson()), file=stdout)
        else:
            click.echo(res.text, file=stdout)
    else:
        raise MapboxCLIException(res.text.strip())
