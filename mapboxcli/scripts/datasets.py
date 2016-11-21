# Datasets.

import json

import click

import mapbox
from mapboxcli.errors import MapboxCLIException


@click.group(short_help="Read and write Mapbox datasets (has subcommands)")
@click.pass_context
def datasets(ctx):
    """Read and write GeoJSON from Mapbox-hosted datasets

    All endpoints require authentication. An access token with
    appropriate dataset scopes is required, see `mapbox --help`.

    Note that this API is currently a limited-access beta.
    """

    access_token = (ctx.obj and ctx.obj.get('access_token')) or None
    service = mapbox.Datasets(access_token=access_token)
    ctx.obj['service'] = service


@datasets.command(short_help="List datasets")
@click.option('--output', '-o', default='-', help="Save output to a file")
@click.pass_context
def list(ctx, output):
    """List datasets.

    Prints a list of objects describing datasets.

        $ mapbox datasets list

    All endpoints require authentication. An access token with
    `datasets:read` scope is required, see `mapbox --help`.
    """

    stdout = click.open_file(output, 'w')
    service = ctx.obj.get('service')
    res = service.list()

    if res.status_code == 200:
        click.echo(res.text, file=stdout)
    else:
        raise MapboxCLIException(res.text.strip())


@datasets.command(short_help="Create an empty dataset")
@click.option('--name', '-n', default=None, help="Name for the dataset")
@click.option('--description', '-d', default=None,
              help="Description for the dataset")
@click.pass_context
def create(ctx, name, description):
    """Create a new dataset.

    Prints a JSON object containing the attributes
    of the new dataset.

        $ mapbox datasets create

    All endpoints require authentication. An access token with
    `datasets:write` scope is required, see `mapbox --help`.
    """

    service = ctx.obj.get('service')
    res = service.create(name, description)

    if res.status_code == 200:
        click.echo(res.text)
    else:
        raise MapboxCLIException(res.text.strip())


@datasets.command(name="read-dataset",
                  short_help="Return information about a dataset")
@click.argument('dataset', required=True)
@click.option('--output', '-o', default='-', help="Save output to a file")
@click.pass_context
def read_dataset(ctx, dataset, output):
    """Read the attributes of a dataset.

    Prints a JSON object containing the attributes
    of a dataset. The attributes: owner (a Mapbox account),
    id (dataset id), created (Unix timestamp), modified
    (timestamp), name (string), and description (string).

        $ mapbox datasets read-dataset dataset-id

    All endpoints require authentication. An access token with
    `datasets:read` scope is required, see `mapbox --help`.
    """

    stdout = click.open_file(output, 'w')
    service = ctx.obj.get('service')
    res = service.read_dataset(dataset)

    if res.status_code == 200:
        click.echo(res.text, file=stdout)
    else:
        raise MapboxCLIException(res.text.strip())


@datasets.command(name="update-dataset",
                  short_help="Update information about a dataset")
@click.argument('dataset', required=True)
@click.option('--name', '-n', default=None, help="Name for the dataset")
@click.option('--description', '-d', default=None,
              help="Description for the dataset")
@click.pass_context
def update_dataset(ctx, dataset, name, description):
    """Update the name and description of a dataset.

    Prints a JSON object containing the updated dataset
    attributes.

        $ mapbox datasets update-dataset dataset-id

    All endpoints require authentication. An access token with
    `datasets:write` scope is required, see `mapbox --help`.
    """

    service = ctx.obj.get('service')
    res = service.update_dataset(dataset, name, description)

    if res.status_code == 200:
        click.echo(res.text)
    else:
        raise MapboxCLIException(res.text.strip())


@datasets.command(name="delete-dataset", short_help="Delete a dataset")
@click.argument('dataset', required=True)
@click.pass_context
def delete_dataset(ctx, dataset):
    """Delete a dataset.

        $ mapbox datasets delete-dataset dataset-id

    All endpoints require authentication. An access token with
    `datasets:write` scope is required, see `mapbox --help`.
    """

    service = ctx.obj.get('service')
    res = service.delete_dataset(dataset)

    if res.status_code != 204:
        raise MapboxCLIException(res.text.strip())


@datasets.command(name="list-features",
                  short_help="List features in a dataset")
@click.argument('dataset', required=True)
@click.option('--reverse', '-r', default=False,
              help="Read features in reverse")
@click.option('--start', '-s', default=None,
              help="Feature id to begin reading from")
@click.option('--limit', '-l', default=None,
              help="Maximum number of features to return")
@click.option('--output', '-o', default='-',
              help="Save output to a file")
@click.pass_context
def list_features(ctx, dataset, reverse, start, limit, output):
    """Get features of a dataset.

    Prints the features of the dataset as a GeoJSON feature collection.

        $ mapbox datasets list-features dataset-id

    All endpoints require authentication. An access token with
    `datasets:read` scope is required, see `mapbox --help`.
    """

    stdout = click.open_file(output, 'w')
    service = ctx.obj.get('service')
    res = service.list_features(dataset, reverse, start, limit)

    if res.status_code == 200:
        click.echo(res.text, file=stdout)
    else:
        raise MapboxCLIException(res.text.strip())


@datasets.command(name="read-feature",
                  short_help="Read a single feature from a dataset")
@click.argument('dataset', required=True)
@click.argument('fid', required=True)
@click.option('--output', '-o', default='-', help="Save output to a file")
@click.pass_context
def read_feature(ctx, dataset, fid, output):
    """Read a dataset feature.

    Prints a GeoJSON representation of the feature.

        $ mapbox datasets read-feature dataset-id feature-id

    All endpoints require authentication. An access token with
    `datasets:read` scope is required, see `mapbox --help`.
    """

    stdout = click.open_file(output, 'w')
    service = ctx.obj.get('service')
    res = service.read_feature(dataset, fid)

    if res.status_code == 200:
        click.echo(res.text, file=stdout)
    else:
        raise MapboxCLIException(res.text.strip())


@datasets.command(name="put-feature",
                  short_help="Insert or update a single feature in a dataset")
@click.argument('dataset', required=True)
@click.argument('fid', required=True)
@click.argument('feature', required=False, default=None)
@click.option('--input', '-i', default='-',
              help="File containing a feature to put")
@click.pass_context
def put_feature(ctx, dataset, fid, feature, input):
    """Create or update a dataset feature.

    The semantics of HTTP PUT apply: if the dataset has no feature
    with the given `fid` a new feature will be created. Returns a
    GeoJSON representation of the new or updated feature.

        $ mapbox datasets put-feature dataset-id feature-id 'geojson-feature'

    All endpoints require authentication. An access token with
    `datasets:write` scope is required, see `mapbox --help`.
    """

    if feature is None:
        stdin = click.open_file(input, 'r')
        feature = stdin.read()

    feature = json.loads(feature)

    service = ctx.obj.get('service')
    res = service.update_feature(dataset, fid, feature)

    if res.status_code == 200:
        click.echo(res.text)
    else:
        raise MapboxCLIException(res.text.strip())


@datasets.command(name="delete-feature",
                  short_help="Delete a single feature from a dataset")
@click.argument('dataset', required=True)
@click.argument('fid', required=True)
@click.pass_context
def delete_feature(ctx, dataset, fid):
    """Delete a feature.

        $ mapbox datasets delete-feature dataset-id feature-id

    All endpoints require authentication. An access token with
    `datasets:write` scope is required, see `mapbox --help`.
    """

    service = ctx.obj.get('service')
    res = service.delete_feature(dataset, fid)

    if res.status_code != 204:
        raise MapboxCLIException(res.text.strip())


@datasets.command(name="create-tileset",
                  short_help="Generate a tileset from a dataset")
@click.argument('dataset', required=True)
@click.argument('tileset', required=True)
@click.option('--name', '-n', default=None, help="Name for the tileset")
@click.pass_context
def create_tileset(ctx, dataset, tileset, name):
    """Create a vector tileset from a dataset.

        $ mapbox datasets create-tileset dataset-id username.data

    Note that the tileset must start with your username and the dataset
    must be one that you own. To view processing status, visit
    https://www.mapbox.com/data/. You may not generate another tilesets
    from the same dataset until the first processing job has completed.

    All endpoints require authentication. An access token with
    `uploads:write` scope is required, see `mapbox --help`.
    """

    access_token = (ctx.obj and ctx.obj.get('access_token')) or None
    service = mapbox.Uploader(access_token=access_token)

    uri = "mapbox://datasets/{username}/{dataset}".format(
        username=tileset.split('.')[0], dataset=dataset)

    res = service.create(uri, tileset, name)

    if res.status_code == 201:
        click.echo(res.text)
    else:
        raise MapboxCLIException(res.text.strip())
