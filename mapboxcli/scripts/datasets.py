# Datasets.

import json
import random
import string
import click
import cligj
import math

from uuid import uuid4

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

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


@datasets.command(name="create-tileset",
                  short_help="Generate a tileset from a dataset")
@click.argument('dataset', required=True)
@click.argument('tileset', required=True)
@click.option('--name', '-n', default=None, help="Name for the tileset")
@click.pass_context
def create_tileset(ctx, dataset, tileset, name):
    """Create a vector tileset from a dataset.

        $ mapbox datasets create-tileset dataset-id username.data

    Note that the tileset must start with your username and the dataset must be
    one that you own which contains data. To view processing status, visit
    https://www.mapbox.com/data/. You may not generate another tilesets from
    the same dataset until the first processing job has completed.

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


@datasets.command(name='list',
                  short_help='List datasets or features in a dataset')
@click.argument('uri', required=True)
@click.pass_context
def ls(ctx, uri):
    """List datasets or features in a dataset.

        $ mapbox datasets list mapbox://datasets/username
        $ mapbox datasets list mapbox://datasets/username/dataset-id

    Use this function to list available datasets, printing their URI, name, and
    description. If a URI for a specific dataset is given, the URIs for
    individual features within that dataset are listed.

    All endpoints require authentication. An access token with
    `uploads:read` scope is required, see `mapbox --help`.
    """

    user, dataset, feature = parse_dataset_uri(uri)

    if feature is not None:
        raise MapboxCLIException("Invalid uri for ls operation {0}".format(uri))

    service = ctx.obj.get('service')

    if dataset is None:
        res = service.list()

        if res.status_code == 200:
            for dataset in json.loads(res.text):
                dataset['name'] = dataset.get('name', None)
                dataset['description'] = dataset.get('description', None)
                click.echo("mapbox://datasets/{owner}/{id}\t{name}: {description}".format(**dataset))
        else:
            raise MapboxCLIException(res.text.strip())

    else:
        for feature in features_gen(service, dataset):
            click.echo("mapbox://datasets/{0}/{1}/{2}".format(user, dataset, feature['id']))


@datasets.command(name="copy",
                  short_help="Move data from one dataset or file to another, overwriting the destination")
@click.argument('source', required=True)
@click.argument('destination', required=True)
@cligj.sequence_opt
@cligj.use_rs_opt
@click.pass_context
def copy_features(ctx, source, destination, sequence, use_rs):
    """Move data from one dataset or file to another, overwriting the
    destination.

    Data to copy is indicated by either a dataset URI, a file path, or - to
    represent stdin/stdout. Below are some example operations:

    To replace dataset-B with the contents of dataset-A:

        \b
        $ mapbox datasets copy \\
        $   mapbox://datasets/username/dataset-A \\
        $   mapbox://datasets/username/dataset-B

    To replace dataset-A with the contents of a local file:

        \b
        $ mapbox datasets copy \\
        $   ~/path/to/my/data.geojson \\
        $   mapbox://datasets/username/dataset-A

    To print the content of a dataset-A to stdout, as line-delimited GeoJSON
    features:

        \b
        $ mapbox datasets copy --sequence \\
        $   mapbox://datasets/username/dataset-A \\
        $   -

    To download all the features in dataset-A to a local file, as a GeoJSON
    FeatureCollection:

        \b
        $ mapbox datasets copy \\
        $   mapbox://datasets/username/dataset-A \\
        $   ~/data.geojson

    To print feature-1 from dataset-A to stdout:

        $ mapbox datasets copy \\
        $   mapbox://datasets/username/dataset-A/feature-1 \\
        $   -

    All endpoints require authentication. An access token with
    `uploads:read` and/or `uploads:write` scope may be required,
    see `mapbox --help`.
    """

    service = ctx.obj.get('service')
    features = get_features(service, source)
    write_features(features, False, sequence, use_rs, service, destination)


@datasets.command(name="append",
                  short_help="Move data from one dataset or file to another, appending to the destination")
@click.argument('source', required=True)
@click.argument('destination', required=True)
@cligj.sequence_opt
@cligj.use_rs_opt
@click.pass_context
def append_features(ctx, source, destination, sequence, use_rs):
    """Move data from one dataset or file to another, appending to the
    destination file or dataset.

    Note that in order to append to a file, the
    file must be a sequence of GeoJSON features and not a FeatureCollection. You
    must specify --sequence in this case.

    Data to copy is indicated by either a dataset URI, a file path, or - to
    represent stdin/stdout. Below are some example operations:

    To append the features from dataset-A to dataset-B:

        \b
        $ mapbox datasets append \\
        $   mapbox://datasets/username/dataset-A \\
        $   mapbox://datasets/username/dataset-B

    To append the features in a local file to dataset-A:

        \b
        $ mapbox datasets append \\
        $   ~/path/to/my/data.geojson \\
        $   mapbox://datasets/username/dataset-A

    To download all the features in dataset-A and append them to a local,
    line-delimited GeoJSON file

        \b
        $ mapbox datasets append --sequence \\
        $   mapbox://datasets/username/dataset-A \\
        $   ~/data.ldgeojson

    All endpoints require authentication. An access token with
    `uploads:read` and/or `uploads:write` scope may be required,
    see `mapbox --help`.
    """

    service = ctx.obj.get('service')
    features = get_features(service, source)
    write_features(features, True, sequence, use_rs, service, destination)


def batch_write_features(service, dataset, features):
    """Perform a single batch feature PUT API call"""

    res = service.batch_update_features(dataset, put=features)

    if res.status_code != 200:
        raise MapboxCLIException(res.text.strip())


def write_features(features, append, sequence, use_rs, service, uri):
    """Write features to a destination, either stdout, a dataset, or a file"""

    try:
        # This will succeed if it is a dataset uri
        user, dataset, fid = parse_dataset_uri(uri)
    except MapboxCLIException:
        # We will be writing to a file or stdout. In append-mode, we can't write
        # FeatureCollection output, so --sequence must be specified
        if append is True and not sequence and uri != "-":
            raise MapboxCLIException('Cannot append to a file without --sequence')

        dst = click.open_file(uri, 'a' if append else 'w')

        if sequence:
            for feature in features:
                if use_rs:
                    click.echo(u'\x1e', nl=False)
                click.echo(json.dumps(feature), file=dst)
        else:
            click.echo(json.dumps(
                {'type': 'FeatureCollection', 'features': list(features)}),
                file=dst)
    else:
        # We will be writing to a dataset. This function performs as many
        # batch write requests as are required to write any number of features
        def write_to_dataset():
            to_put = []
            for feature in features:
                if feature.get('id') is None:
                    feature['id'] = uuid4().hex

                to_put.append(feature)

                if len(to_put) == 100:
                    batch_write_features(service, dataset, to_put)
                    to_put = []

            if len(to_put) > 0:
                batch_write_features(service, dataset, to_put)

        if append is True:
            # If we are in append-mode, just write the features to the dataset
            return write_to_dataset()

        # Otherwise, we're overwriting a dataset. First we need to purge all the
        # existing features, then write the new ones
        def list_features(start=None):
            res = service.list_features(dataset, start=start)

            if res.status_code != 200:
                raise MapboxCLIException(res.text.strip())

            collection = json.loads(res.text)

            if len(collection['features']) != 0:
                ids = [feature['id'] for feature in collection['features']]
                purge_features(ids)
                list_features(ids[-1])
            else:
                write_to_dataset()

        def purge_features(ids):
            res = service.batch_update_features(dataset, delete=ids)

            if res.status_code != 200:
                raise MapboxCLIException(res.text.strip())

        list_features()


def get_features(service, uri):
    """Get features from stdin, a dataset, or a file"""

    try:
        user, dataset, fid = parse_dataset_uri(uri)
    except MapboxCLIException:
        src = iter(click.open_file(uri, 'r'))
        for feature in cligj.features.iter_features(src):
            yield feature
    else:
        if dataset is None:
            raise MapboxCLIException("Invalid dataset uri {0}".format(uri))
        elif fid:
            res = service.read_feature(dataset, fid)

            if res.status_code == 200:
                yield json.loads(res.text)
            else:
                raise MapboxCLIException(res.text.strip())

        else:
            for feature in features_gen(service, dataset):
                yield feature


def parse_dataset_uri(uri):
    """Parse a dataset uri, returning user, dataset id, and feature id"""

    parsed = urlparse(uri)

    if parsed.scheme != 'mapbox' or parsed.netloc != 'datasets':
        raise MapboxCLIException("Invalid dataset uri {0}".format(uri))

    path = parsed.path[1:].split('/')
    if len(path) < 1 or len(path) > 3:
        raise MapboxCLIException("Invalid dataset uri {0}".format(uri))
    elif len(path) == 1:
        path = path + [None, None]
    elif len(path) == 2:
        path = path + [None]

    return path


def features_list(service, dataset, reverse=None, start=None):
    """Makes one API request, returns a list of features"""

    res = service.list_features(dataset, reverse, start)

    if res.status_code != 200:
        raise MapboxCLIException(res.text.strip())

    return json.loads(res.text)['features']


def features_gen(service, dataset, reverse=None, start=None):
    """Generator function to make a number of API requests and yield features"""

    features = features_list(service, dataset, reverse, start)

    while len(features) > 0:
        for feature in features:
            yield feature

        last = features[-1]['id']
        features = features_list(service, dataset, reverse, last)
