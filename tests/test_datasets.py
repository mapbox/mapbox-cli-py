import base64
import json
import tempfile

from click.testing import CliRunner
import responses

from mapboxcli.scripts.cli import main_group
from mapboxcli.scripts import datasets
from mapboxcli.errors import MapboxCLIException

import mapbox

username = 'testuser'
access_token = 'sk.{0}.test'.format(
    base64.b64encode(b'{"u":"testuser"}').decode('utf-8'))
service = mapbox.Datasets(access_token=access_token)

null_island = {
    "type": "FeatureCollection",
    "features": [
        {
            "id": "a",
            "type": "Feature",
            "properties": {"name": "Null"},
            "geometry": {"type": "Point", "coordinates": [0, 0]}
        }
    ]
}


@responses.activate
def test_cli_datasets_create_tileset():
    dataset = "dataset-1"
    name = "test"
    tileset = "testuser.data"
    owner = tileset.split('.')[0]

    expected = """{{
        "id":"ciiae5gc40041mblzuluvu7jr",
        "name":"{0}",
        "complete":false,
        "error":null,
        "created":"2015-12-17T15:17:46.703Z",
        "modified":"2015-12-17T15:17:46.703Z",
        "tileset":"{1}",
        "owner":"{2}",
        "progress":0
    }}""".format(name, tileset, owner)

    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}?access_token={1}'.format(
            owner, access_token
        ),
        status=201, body=expected,
        match_querystring=True,
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'create-tileset',
         dataset,
         tileset,
         '--name', name])

    assert result.exit_code == 0
    body = json.loads(responses.calls[0].request.body)
    assert body['url'] == 'mapbox://datasets/{0}/{1}'.format(owner, dataset)
    assert body['tileset'] == tileset
    assert body['name'] == name


@responses.activate
def test_cli_datasets_list_datasets():
    datasets = """
        [
         {{
          "owner":"{username}",
          "id":"120c1c5aec87030449dfe2dff4e2a7c8",
          "name":"first",
          "description":"the first one",
          "created":"2015-07-03T00:14:09.622Z",
          "modified":"2015-07-03T00:14:09.622Z"
         }},
         {{
          "owner":"{username}",
          "name":"second",
          "description":"the second one",
          "id":"18571b87d4c139b6d10911d13cb0561f",
          "created":"2015-05-05T22:43:10.832Z",
          "modified":"2015-05-05T22:43:10.832Z"
         }}
        ]""".format(username=username)

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}?access_token={1}'.format(
            username, access_token
        ),
        match_querystring=True,
        body=datasets, status=200,
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'list',
         'mapbox://datasets/{0}'.format(username)])

    assert result.exit_code == 0

    output = result.output.splitlines()
    assert len(output) == 2
    assert output[0] == "mapbox://datasets/{0}/120c1c5aec87030449dfe2dff4e2a7c8\tfirst: the first one".format(username)
    assert output[1] == "mapbox://datasets/{0}/18571b87d4c139b6d10911d13cb0561f\tsecond: the second one".format(username)


@responses.activate
def test_cli_datasets_list_features():
    dataset = "abc"
    features = """
        {
          "type": "FeatureCollection",
          "features": [{
            "type":"Feature",
            "id":"a",
            "properties":{},
            "geometry":{"type":"Point","coordinates":[0,0]}
          }, {
              "type":"Feature",
              "id":"b",
              "properties":{},
              "geometry":{"type":"Point","coordinates":[1,1]}
          }]
        }"""

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{2}/features?access_token={1}'
        .format(username, access_token, dataset),
        match_querystring=True,
        body=features, status=200,
        content_type='application/json'
    )

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{2}/features?access_token={1}&start=b'
        .format(username, access_token, dataset),
        match_querystring=True,
        body="""{"type":"FeatureCollection","features":[]}""",
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'list',
         'mapbox://datasets/{0}/{1}'.format(username, dataset)])

    assert result.exit_code == 0

    output = result.output.splitlines()
    assert len(output) == 2
    assert output[0] == "mapbox://datasets/{0}/abc/a".format(username)
    assert output[1] == "mapbox://datasets/{0}/abc/b".format(username)

    assert len(responses.calls) == 2


@responses.activate
def test_cli_datasets_copy_file_to_dataset():
    dataset = "abc"

    # first it will list the dataset's features ...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'
        .format(username, dataset, access_token),
        match_querystring=True,
        body=json.dumps(null_island),
        content_type='application/json'
    )

    # ... then it will batch delete ...
    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'
        .format(username, dataset, access_token),
        match_querystring=True,
        body='{"put":[],"delete":["a"]}',
        content_type='application/json'
    )

    # ... then it will paginate ...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}&start=a'
        .format(username, dataset, access_token),
        match_querystring=True,
        body='{"type":"FeatureCollection","features":[]}',
        content_type='application/json'
    )

    # ... then it will write new features
    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'
        .format(username, dataset, access_token),
        match_querystring=True,
        body='{"put":[],"delete":[]}',
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'copy',
         './examples/cities.geojson',
         'mapbox://datasets/{0}/{1}'.format(username, dataset)])

    assert result.exit_code == 0

    assert responses.calls[0].request.method == 'GET'
    assert responses.calls[1].request.method == 'POST'
    assert responses.calls[1].request.body == '{"delete": ["a"]}'
    assert responses.calls[2].request.method == 'GET'
    assert responses.calls[3].request.method == 'POST'

    found = json.loads(responses.calls[3].request.body)
    fixture = open('./examples/cities.geojson', 'r')
    expected = {"put": json.loads(fixture.read())['features']}
    assert found == expected


@responses.activate
def test_cli_datasets_copy_dataset_to_file():
    dataset = "abc"
    tmp, filepath = tempfile.mkstemp()

    # first it will list the dataset's features ...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(username, dataset, access_token),
        match_querystring=True,
        body=json.dumps(null_island),
        content_type='application/json'
    )

    # ... then it will paginate.
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}&start=a'
        .format(username, dataset, access_token),
        match_querystring=True,
        body='{"type":"FeatureCollection","features":[]}',
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'copy',
         'mapbox://datasets/{0}/{1}'.format(username, dataset),
         filepath])

    assert result.exit_code == 0
    assert json.loads(open(filepath, 'r').read()) == null_island


@responses.activate
def test_cli_datasets_copy_feature_to_stdout():
    dataset = "abc"
    fid = "def"

    # first it will list the dataset's features ...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features/{3}?access_token={2}'
        .format(username, dataset, access_token, fid),
        match_querystring=True,
        body=json.dumps(null_island['features'][0]),
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'copy',
         'mapbox://datasets/{0}/{1}/{2}'.format(username, dataset, fid),
         '-'])

    assert result.exit_code == 0
    print(result.output)
    assert json.loads(result.output) == {"type": "FeatureCollection", "features": [null_island['features'][0]]}


@responses.activate
def test_cli_datasets_copy_dataset_to_stdout():
    dataset = "abc"

    # first it will list the dataset's features ...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'
        .format(username, dataset, access_token),
        match_querystring=True,
        body=json.dumps(null_island),
        content_type='application/json'
    )

    # ... then it will paginate.
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}&start=a'
        .format(username, dataset, access_token),
        match_querystring=True,
        body='{"type":"FeatureCollection","features":[]}',
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'copy',
         'mapbox://datasets/{0}/{1}'.format(username, dataset),
         '-'])

    assert result.exit_code == 0
    assert json.loads(result.output) == null_island


@responses.activate
def test_cli_datasets_copy_dataset_to_dataset():
    datasetA = "abc"
    datasetB = "def"

    # first it will list the dataset B's features ...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'
        .format(username, datasetB, access_token),
        match_querystring=True,
        body=json.dumps(null_island),
        content_type='application/json'
    )

    # ... then it will batch delete ...
    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'
        .format(username, datasetB, access_token),
        match_querystring=True,
        body='{"put":[],"delete":["a"]}',
        content_type='application/json'
    )

    # ... then it will paginate ...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}&start=a'
        .format(username, datasetB, access_token),
        match_querystring=True,
        body='{"type":"FeatureCollection","features":[]}',
        content_type='application/json'
    )

    # ... then it will list dataset A's features...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'
        .format(username, datasetA, access_token),
        match_querystring=True,
        body=json.dumps(null_island),
        content_type='application/json'
    )

    # ... paginate ...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}&start=a'
        .format(username, datasetA, access_token),
        match_querystring=True,
        body='{"type":"FeatureCollection","features":[]}',
        content_type='application/json'
    )

    # ... then it will write new features
    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'
        .format(username, datasetB, access_token),
        match_querystring=True,
        body='{"put":[],"delete":[]}',
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'copy',
         'mapbox://datasets/{0}/{1}'.format(username, datasetA),
         'mapbox://datasets/{0}/{1}'.format(username, datasetB)])

    assert result.exit_code == 0

    assert responses.calls[0].request.method == 'GET'  # list dataset B
    assert responses.calls[1].request.method == 'POST'  # batch delete from dataset B
    assert responses.calls[1].request.body == '{"delete": ["a"]}'
    assert responses.calls[2].request.method == 'GET'  # paginate dataset B
    assert responses.calls[3].request.method == 'GET'  # list dataset A
    assert responses.calls[4].request.method == 'GET'  # paginate dataset A
    assert responses.calls[5].request.method == 'POST'  # batch write dataset B

    found = json.loads(responses.calls[5].request.body)
    expected = {"put": [null_island['features'][0]]}
    assert found == expected


@responses.activate
def test_cli_datasets_append_file_to_dataset():
    dataset = "abc"

    # should just write new features
    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(username, dataset, access_token),
        match_querystring=True,
        body='{"put":[],"delete":[]}',
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'append',
         './examples/cities.geojson',
         'mapbox://datasets/{0}/{1}'.format(username, dataset)])

    assert result.exit_code == 0

    assert responses.calls[0].request.method == 'POST'

    found = json.loads(responses.calls[0].request.body)
    fixture = open('./examples/cities.geojson', 'r')
    expected = {"put": json.loads(fixture.read())['features']}
    assert found == expected


@responses.activate
def test_cli_datasets_append_dataset_to_file():
    dataset = "abc"
    tmp, filepath = tempfile.mkstemp()

    # first it will list the dataset's features ...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(username, dataset, access_token),
        match_querystring=True,
        body=json.dumps(null_island),
        content_type='application/json'
    )

    # ... then it will paginate.
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}&start=a'.format(username, dataset, access_token),
        match_querystring=True,
        body='{"type":"FeatureCollection","features":[]}',
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'append',
         'mapbox://datasets/{0}/{1}'.format(username, dataset),
         filepath])

    assert result.exit_code == 1

    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'append',
         '--sequence',
         'mapbox://datasets/{0}/{1}'.format(username, dataset),
         filepath])

    assert result.exit_code == 0
    assert json.loads(open(filepath, 'r').read()) == null_island['features'][0]


@responses.activate
def test_cli_datasets_append_dataset_to_dataset():
    datasetA = "abc"
    datasetB = "def"

    # first it will list dataset A's features...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(username, datasetA, access_token),
        match_querystring=True,
        body=json.dumps(null_island),
        content_type='application/json'
    )

    # ... paginate ...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}&start=a'.format(username, datasetA, access_token),
        match_querystring=True,
        body='{"type":"FeatureCollection","features":[]}',
        content_type='application/json'
    )

    # ... then it will write new features
    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(username, datasetB, access_token),
        match_querystring=True,
        body='{"put":[],"delete":[]}',
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'append',
         'mapbox://datasets/{0}/{1}'.format(username, datasetA),
         'mapbox://datasets/{0}/{1}'.format(username, datasetB)])

    assert result.exit_code == 0

    assert responses.calls[0].request.method == 'GET'  # list dataset A
    assert responses.calls[1].request.method == 'GET'  # paginate dataset A
    assert responses.calls[2].request.method == 'POST'  # batch write dataset B

    found = json.loads(responses.calls[2].request.body)
    expected = {"put": [null_island['features'][0]]}
    assert found == expected


@responses.activate
def test_datasets_batch_write_features():
    dataset = "abc"
    features = [
        {
            "type": "Feature",
            "id": "a",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [0, 0]
            }
        }, {
            "type": "Feature",
            "id": "b",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [1, 1]
            }
        }
    ]

    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'
        .format(username, dataset, access_token),
        match_querystring=True,
        body=json.dumps({"put": features, "delete": []}),
        content_type='application/json'
    )

    datasets.batch_write_features(service, dataset, features)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.method == 'POST'
    assert json.loads(responses.calls[0].request.body) == {"put": features}


@responses.activate
def test_datasets_batch_write_features_exception():
    dataset = 'abc'

    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(username, dataset, access_token),
        match_querystring=True,
        body=json.dumps({"Message": "humbug"}),
        content_type='application/json',
        status=401
    )

    try:
        datasets.batch_write_features(service, dataset, ["bah"])
    except MapboxCLIException:
        assert True
    else:
        assert False


@responses.activate
def test_datasets_write_features_append_to_dataset():
    dataset = 'abc'
    features = []
    for i in range(1, 124):
        features.append({
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [180 % i, 90 % i]
            }
        })

    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(username, dataset, access_token),
        match_querystring=True,
        body=json.dumps({"put": [], "delete": []}),
        content_type='application/json'
    )

    datasets.write_features(
        features,
        True,
        None,
        None,
        service,
        'mapbox://datasets/{0}/{1}'.format(username, dataset)
    )

    assert len(responses.calls) == 2
    for call in responses.calls:
        assert call.request.method == 'POST'

    first = json.loads(responses.calls[0].request.body)
    assert len(first['put']) == 100

    for f in first['put']:
        assert len(f['id']) == 32  # auto-assigned ids

    second = json.loads(responses.calls[1].request.body)
    assert len(second['put']) == 23

    for f in second['put']:
        assert len(f['id']) == 32


@responses.activate
def test_datasets_write_features_copy_to_dataset():
    dataset = 'abc'
    features = []
    for i in range(1, 124):
        features.append({
            "type": "Feature",
            "id": str(i),
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [180 % i, 90 % i]
            }
        })

    # first it will list the dataset's features ...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'
        .format(username, dataset, access_token),
        match_querystring=True,
        body=json.dumps(null_island),
        content_type='application/json'
    )

    # ... then it will batch delete ...
    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'
        .format(username, dataset, access_token),
        match_querystring=True,
        body='{"put":[],"delete":["a"]}',
        content_type='application/json'
    )

    # ... then it will paginate ...
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}&start=a'.format(username, dataset, access_token),
        match_querystring=True,
        body='{"type":"FeatureCollection","features":[]}',
        content_type='application/json'
    )

    # ... and then start posting new features
    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(username, dataset, access_token),
        match_querystring=True,
        body=json.dumps({"put": [], "delete": []}),
        content_type='application/json'
    )

    datasets.write_features(
        features,
        False,
        None,
        None,
        service,
        'mapbox://datasets/{0}/{1}'.format(username, dataset)
    )

    assert len(responses.calls) == 5

    methods = [call.request.method for call in responses.calls]
    assert methods == ['GET', 'POST', 'GET', 'POST', 'POST']

    first = json.loads(responses.calls[3].request.body)
    assert len(first['put']) == 100

    for f in first['put']:
        assert len(f['id']) < 4  # did not auto-assign ids

    second = json.loads(responses.calls[4].request.body)
    assert len(second['put']) == 23

    for f in second['put']:
        assert len(f['id']) < 4


def test_datasets_write_features_append_to_file_without_sequence():
    tmp, filepath = tempfile.mkstemp()

    try:
        datasets.write_features([], True, None, None, service, filepath)
    except MapboxCLIException:
        assert True
    else:
        assert False


def test_datasets_write_features_append_to_file():
    tmp, filepath = tempfile.mkstemp()

    with open(filepath, 'w') as f:
        f.write('first line\n')

    datasets.write_features(null_island['features'], True, True, None, service, filepath)

    with open(filepath, 'r') as f:
        data = f.read()

    assert data.startswith('first line\n')


def test_datasets_write_features_overwrite_file():
    tmp, filepath = tempfile.mkstemp()

    with open(filepath, 'w') as f:
        f.write('first line\n')

    datasets.write_features(null_island['features'], False, True, None, service, filepath)

    with open(filepath, 'r') as f:
        data = f.read()

    assert not data.startswith('first line\n')


def test_datasets_write_features_stdout_sequence(capsys):
    datasets.write_features(null_island['features'], False, True, None, service, '-')
    out, err = capsys.readouterr()
    assert out == json.dumps(null_island['features'][0]) + '\n'


def test_datasets_write_features_file_rs(capsys):
    tmp, filepath = tempfile.mkstemp()
    datasets.write_features(
        [null_island['features'][0], null_island['features'][0]],
        False,
        True,
        True,
        service,
        '-'
    )

    out, err = capsys.readouterr()
    island = json.dumps(null_island['features'][0]) + '\n'

    assert out.split(u'\x1e') == ['', island, island]


def test_datasets_write_feature_stdout_collection(capsys):
    datasets.write_features(null_island['features'], False, None, None, service, '-')
    out, err = capsys.readouterr()
    assert json.loads(out) == null_island
