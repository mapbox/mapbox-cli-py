import json
import re

import click
import cligj

import mapbox
from mapboxcli.errors import MapboxCLIException


def waypoint_snapping_callback(ctx, param, value):
    results = []

    tuple_pattern = re.compile("[,]")
    int_pattern = re.compile("[0-9]")

    # value is an n-tuple, each element of
    # which contains input from the user.
    #
    # Iterate over each element, determining
    # whether to convert it to a tuple,
    # convert it to an int, or leave it as
    # a str.
    #
    # Append each element to results, which
    # the Directions SDK will attempt to
    # validate.

    if len(value) == 0:
        return None

    for element in value:

        # If the element contains a comma, then assume 
        # that the user intended to pass in a tuple.
        #
        # Convert each item in the element to an int,
        # and create a tuple containing all items.
        #
        # Raise an error if the item is not a valid int.
        #
        # (The SDK accepts a three-tuple with ints for 
        # radius, angle, and range.)

        if re.search(tuple_pattern, element):
            element = re.split(tuple_pattern, element)

            for index in range(0, len(element)):
                try:
                    element[index] = int(element[index])
                except ValueError as exc:
                    raise mapbox.errors.ValidationError(str(exc))

            element = tuple(element)

            results.append(element)

        # If the element contains a decimal number but not 
        # a comma, then assume that the user intended to 
        # pass in an int.
        #
        # Convert the element to an int.
        #
        # Raise an error if the item is not a valid int.
        #
        # (The Directions SDK accepts an int for radius.)

        elif re.search(int_pattern, element):
            try:
                element = int(element)
            except ValueError as exc:
                raise mapbox.errors.ValidationError(str(exc))
      
            results.append(element)

        # If the element contains neither a decimal number
        # nor a comma, then assume that the user intended 
        # to pass in a str.
        #
        # Do nothing since the element is already a str.
        #
        # (The Directions SDK accepts a str for unlimited radius.)

        else:
            results.append(element)

    return results


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

# Directions.valid_geom_overview contains two 
# elements of type str and one element of type bool.  
# This causes the Directions CLI's --help option to 
# raise a TypeError.  To prevent this, we convert
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
    "--waypoint-snapping",
    multiple=True,
    callback=waypoint_snapping_callback,
    help="Controls waypoint snapping"
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
               waypoint_snapping, annotations, language, output):
    """The Mapbox Directions API will show you how to get
       where you're going.

       mapbox directions "[0, 0]" "[1, 1]"

       An access token is required.  See "mapbox --help".
    """

    access_token = (ctx.obj and ctx.obj.get("access_token")) or None

    service = mapbox.Directions(access_token=access_token)

    # The Directions SDK expects False to be
    # a bool, not a str.

    if overview == "False":
        overview = False

    # When using waypoint snapping, the 
    # Directions SDK expects features to be 
    # a list, not a generator.

    if waypoint_snapping is not None:
        features = list(features)

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
            waypoint_snapping=waypoint_snapping,
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
