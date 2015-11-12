import click


@click.command(short_help="Routing between waypoints.")
@click.argument('waypoints', default='-', nargs=-1, required=True)
@click.option('--profile', default="mapbox.driving", type=click.Choice([
              'mapbox.driving', 'mapbox.walking', 'mapbox.cycling']),
              help="Mapbox direction profile id")
@click.option('--alternatives/--no-alternatives', default=True,
              help="Generate alternative routes?")
@click.option('--instructions', default="text", type=click.Choice(["text", "html"]),
              help="Format for route instructions")
@click.option('--geometry', default="geojson", type=click.Choice([
              'geojson', 'polyline', 'false']), help="Geometry encoding")
@click.option('--steps/--no-steps', default=False,
              help="Include steps in the response")
@click.option('--geojson/--no-geojson', default=False,
              help="Return geojson feature collection (default: full response json)")
@click.option('--output', '-o', default='-',
              help="Save output to a file.")
@click.pass_context
def directions(ctx, waypoints, geojson, profile, alternatives,
               instructions, geometry, steps, output):
    """Calculate optimal route with turn-by-turn directions
    between up to 25 waypoints.

      $ mbx directions "[-122.681032, 45.528334]" "[-122.71679, 45.525135]"

    An access token is required, see `mbx --help`.
    """
    pass
