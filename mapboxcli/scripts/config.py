import click


@click.command(short_help="Show all config settings.")
@click.pass_context
def config(ctx):
    click.echo("[mapbox]")
    click.echo("access-token = {0}".format(ctx.obj['access_token']))
    click.echo("verbosity = {0}".format(ctx.obj['verbosity']))
