import click

@click.command(short_help="Upload datasets to Mapbox accounts")
@click.argument('username', required=True)
@click.argument('input', nargs=1, required=True)
@click.argument('tileset', required=True)
@click.option('--name', help="Name for the data upload")
@click.pass_context
def uploads(ctx, waypoints, geojson, profile, alternatives,
            instructions, geometry, steps, output):
    """Upload data to Mapbox accounts.
    All endpoints require authentication.
    Uploaded data lands at https://www.mapbox.com/data/
    and can be used in new or existing projects.

      $ mbx uploads username data.geojson username.data

    An access token with upload scope is required, see `mbx --help`.
    """
    pass
