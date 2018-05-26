import click
from json import dumps
import mapbox
from mapboxcli.errors import MapboxCLIException

@click.command(
  short_help="Returns the counts per day for a given resource and period."
)

@click.option(
  "--resource-type", 
  "-t", 
  type=click.Choice(mapbox.Analytics.valid_resource_types), 
  required=True,
  help="The resource being requested."
)

@click.option(
  "--username", 
  "-u", 
  type=str, 
  required=True,
  help="The username for the account that owns the resource."
)

@click.option(
  "--id", 
  "-i", 
  type=str,
  help="The id for the resource."
)

@click.option(
  "--start", 
  "-s", 
  type=str,
  help="The ISO-formatted start date."
)

@click.option(
  "--end", 
  "-e", 
  type=str,
  help="The ISO-formatted end date."
)

@click.pass_context
def analytics(ctx, resource_type, username, id, start, end):
  """The Mapbox Analytics API returns the counts per day for
     a given resource and period.


     Long options:

     $ mapbox analytics --resource-type <resource type> --username <username> --id <resource id> --start <ISO-formatted start date> --end <ISO-formatted end date>

     Short options:

     $ mapbox analytics -t <resource type> -u <username> -i <resource id> -s <ISO-formatted start date> -e <ISO-formatted end date>


     An access token is required.  See "mapbox --help".
  """

  access_token = (ctx.obj and ctx.obj.get("access_token")) or None

  service = mapbox.Analytics(access_token=access_token)

  try:
    res = service.analytics(
      resource_type, 
      username, 
      id=id, 
      start=start, 
      end=end
    )
  except mapbox.errors.ValidationError as exc:
    raise click.BadParameter(str(exc))

  if res.status_code == 200:
    click.echo(dumps(res.json()))
  else:
    raise MapboxCLIException(res.text.strip())
