# Datasets.

import json
import click

import mapbox
from mapboxcli.errors import MapboxCLIException


@click.group(short_help="Low-level read and write functions for Mapbox datasets (has subcommands)")
@click.pass_context
def datasetsapi(ctx):
    """Low-level read and write functions for Mapbox datasets

    All endpoints require authentication. An access token with
    appropriate dataset scopes is required, see `mapbox --help`.

    Note that this API is currently a limited-access beta.
    """

    access_token = (ctx.obj and ctx.obj.get('access_token')) or None
    service = mapbox.Datasets(access_token=access_token)
    ctx.obj['service'] = service


@datasetsapi.command(name="list-datasets", short_help="List datasets")
@click.option('--output', '-o', default='-', help="Save output to a file")
@click.pass_context
def list_datasets(ctx, output):
    """List datasets.

    Prints a list of objects describing datasets.

        $ mapbox datasetsapi list-datasets

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


@datasetsapi.command(name="create-dataset", short_help="Create an empty dataset")
@click.option('--name', '-n', default=None, help="Name for the dataset")
@click.option('--description', '-d', default=None,
              help="Description for the dataset")
@click.pass_context
def create_dataset(ctx, name, description):
    """Create a new dataset.

    Prints a JSON object containing the attributes
    of the new dataset.

        $ mapbox datasetsapi create-dataset

    All endpoints require authentication. An access token with
    `datasets:write` scope is required, see `mapbox --help`.
    """

    service = ctx.obj.get('service')
    res = service.create(name, description)

    if res.status_code == 200:
        click.echo(res.text)
    else:
        raise MapboxCLIException(res.text.strip())


@datasetsapi.command(
    name="read-dataset", short_help="Return information about a dataset")
@click.argument('dataset', required=True)
@click.option('--output', '-o', default='-', help="Save output to a file")
@click.pass_context
def read_dataset(ctx, dataset, output):
    """Read the attributes of a dataset.

    Prints a JSON object containing the attributes
    of a dataset. The attributes: owner (a Mapbox account),
    id (dataset id), created (Unix timestamp), modified
    (timestamp), name (string), and description (string).

        $ mapbox datasetsapi read-dataset dataset-id

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


@datasetsapi.command(
    name="update-dataset", short_help="Update information about a dataset")
@click.argument('dataset', required=True)
@click.option('--name', '-n', default=None, help="Name for the dataset")
@click.option('--description', '-d', default=None,
              help="Description for the dataset")
@click.pass_context
def update_dataset(ctx, dataset, name, description):
    """Update the name and description of a dataset.

    Prints a JSON object containing the updated dataset
    attributes.

        $ mapbox datasetsapi update-dataset dataset-id

    All endpoints require authentication. An access token with
    `datasets:write` scope is required, see `mapbox --help`.
    """

    service = ctx.obj.get('service')
    res = service.update_dataset(dataset, name, description)

    if res.status_code == 200:
        click.echo(res.text)
    else:
        raise MapboxCLIException(res.text.strip())


@datasetsapi.command(name="delete-dataset", short_help="Delete a dataset")
@click.argument('dataset', required=True)
@click.pass_context
def delete_dataset(ctx, dataset):
    """Delete a dataset.

        $ mapbox datasetsapi delete-dataset dataset-id

    All endpoints require authentication. An access token with
    `datasets:write` scope is required, see `mapbox --help`.
    """

    service = ctx.obj.get('service')
    res = service.delete_dataset(dataset)

    if res.status_code != 204:
        raise MapboxCLIException(res.text.strip())


@datasetsapi.command(
    name="list-features", short_help="List one page of features from a dataset")
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

        $ mapbox datasetsapi list-features dataset-id

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


@datasetsapi.command(
    name="read-feature", short_help="Read a single feature from a dataset")
@click.argument('dataset', required=True)
@click.argument('fid', required=True)
@click.option('--output', '-o', default='-', help="Save output to a file")
@click.pass_context
def read_feature(ctx, dataset, fid, output):
    """Read a dataset feature.

    Prints a GeoJSON representation of the feature.

        $ mapbox datasetsapi read-feature dataset-id feature-id

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


@datasetsapi.command(
    name="put-feature", short_help="Insert or update a single feature in a dataset")
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

        $ mapbox datasetsapi put-feature dataset-id feature-id 'geojson-feature'

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


@datasetsapi.command(
    name="delete-feature", short_help="Delete a single feature from a dataset")
@click.argument('dataset', required=True)
@click.argument('fid', required=True)
@click.pass_context
def delete_feature(ctx, dataset, fid):
    """Delete a feature.

        $ mapbox datasetsapi delete-feature dataset-id feature-id

    All endpoints require authentication. An access token with
    `datasets:write` scope is required, see `mapbox --help`.
    """

    service = ctx.obj.get('service')
    res = service.delete_feature(dataset, fid)

    if res.status_code != 204:
        raise MapboxCLIException(res.text.strip())


@datasetsapi.command(
    name="batch-update-features",
    short_help="Insert, update, or delete multiple features in a dataset")
@click.argument('dataset', required=True)
@click.argument('puts', required=False, default=None)
@click.argument('deletes', required=False, default=None)
@click.option(
    '--input', '-i', default='-',
    help="File containing features to insert, update, and/or delete")
@click.pass_context
def batch_update_features(ctx, dataset, puts, deletes, input):
    """Update features of a dataset.

    Up to 100 features may be deleted or modified in one request. PUTS
    should be a JSON array of GeoJSON features to insert or updated.
    DELETES should be a JSON array of feature ids to be deleted.

        $ mapbox datasetsapi batch-update-features dataset-id 'puts' 'deletes'

    All endpoints require authentication. An access token with
    `datasets:write` scope is required, see `mapbox --help`.
    """

    if puts:
        puts = json.loads(puts)

    if deletes:
        deletes = json.loads(deletes)

    if puts is None and deletes is None:
        stdin = click.open_file(input, 'r')
        input = json.loads(stdin.read())
        puts = input['put']
        deletes = input['delete']

    service = ctx.obj.get('service')
    res = service.batch_update_features(dataset, puts, deletes)

    if res.status_code == 200:
        click.echo(res.text)
    else:
        raise MapboxCLIException(res.text.strip())
