import base64
import re
import json

from click.testing import CliRunner
import responses

from mapboxcli.scripts.cli import main_group
import mapbox

username = 'testuser'
access_token = 'sk.{0}.test'.format(
    base64.b64encode(b'{"u":"testuser"}').decode('utf-8'))

@responses.activate
def test_cli_dataset_list_stdout():
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
          "description":"the second one"
          "id":"18571b87d4c139b6d10911d13cb0561f",
          "created":"2015-05-05T22:43:10.832Z",
          "modified":"2015-05-05T22:43:10.832Z"
         }}
        ]""".format(username=username)

    datasets = "".join(datasets.split())

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body=datasets, status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'list'])

    assert result.exit_code == 0
    assert result.output.strip() == datasets.strip()

@responses.activate
def test_cli_dataset_list_tofile(tmpdir):
    tmpfile = str(tmpdir.join('test.list.json'))

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
          "description":"the second one"
          "id":"18571b87d4c139b6d10911d13cb0561f",
          "created":"2015-05-05T22:43:10.832Z",
          "modified":"2015-05-05T22:43:10.832Z"
         }}
        ]""".format(username=username)

    datasets = "".join(datasets.split())

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body=datasets, status=200,
        content_type='application/json')


    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'list',
         '--output', tmpfile])

    assert result.exit_code == 0
    assert open(tmpfile).read().strip() == datasets.strip()
    assert result.output.strip() == ""

@responses.activate
def test_cli_dataset_create_noargs():
    created = """
    {{"owner":"{username}",
      "id":"cii9dtexw0039uelz7nzk1lq3",
      "name":null,
      "description":null,
      "created":"2015-12-16T22:20:38.847Z",
      "modified":"2015-12-16T22:20:38.847Z"}}
    """.format(username=username)

    created = "".join(created.split())

    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body=created, status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'create'])

    assert result.exit_code == 0
    assert result.output.strip() == created.strip()

@responses.activate
def test_cli_dataset_create_withargs():
    name = "the-name"
    description = "the-description"
    created = """
    {{"owner":"{username}",
      "id":"cii9dtexw0039uelz7nzk1lq3",
      "name":{name},
      "description":{description},
      "created":"2015-12-16T22:20:38.847Z",
      "modified":"2015-12-16T22:20:38.847Z"}}
    """.format(username=username, name=name, description=description)

    created = "".join(created.split())

    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body=created, status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'create',
         '--name', name,
         '-d', description])

    assert result.exit_code == 0
    assert result.output.strip() == created.strip()

@responses.activate
def test_cli_dataset_read_dataset_stdout():
    id = "cii9dtexw0039uelz7nzk1lq3"
    created = """
    {{"owner":"{username}",
      "id":"{id}",
      "name":null,
      "description":null,
      "created":"2015-12-16T22:20:38.847Z",
      "modified":"2015-12-16T22:20:38.847Z"}}
    """.format(username=username, id=id)

    created = "".join(created.split())

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}?access_token={2}'.format(username, id, access_token),
        match_querystring=True,
        body=created, status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'read-dataset', id])

    assert result.exit_code == 0
    assert result.output.strip() == created.strip()

@responses.activate
def test_cli_dataset_read_dataset_tofile(tmpdir):
    tmpfile = str(tmpdir.join('test.read-dataset.json'))
    id = "cii9dtexw0039uelz7nzk1lq3"
    created = """
    {{"owner":"{username}",
      "id":"{id}",
      "name":null,
      "description":null,
      "created":"2015-12-16T22:20:38.847Z",
      "modified":"2015-12-16T22:20:38.847Z"}}
    """.format(username=username, id=id)

    created = "".join(created.split())

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}?access_token={2}'.format(username, id, access_token),
        match_querystring=True,
        body=created, status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'read-dataset', id,
         '-o', tmpfile])

    assert result.exit_code == 0
    assert open(tmpfile).read().strip() == created.strip()

@responses.activate
def test_cli_dataset_update_dataset():
    id = "cii9dtexw0039uelz7nzk1lq3"
    name = "the-name"
    description = "the-description"
    created = """
    {{"owner":"{username}",
      "id":"{id}",
      "name":{name},
      "description":{description},
      "created":"2015-12-16T22:20:38.847Z",
      "modified":"2015-12-16T22:20:38.847Z"}}
    """.format(username=username, id=id, name=name, description=description)

    created = "".join(created.split())

    responses.add(
        responses.PATCH,
        'https://api.mapbox.com/datasets/v1/{0}/{1}?access_token={2}'.format(username, id, access_token),
        match_querystring=True,
        body=created, status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'update-dataset', id,
         '--name', name,
         '-d', description])

    assert result.exit_code == 0
    assert result.output.strip() == created.strip()

@responses.activate
def test_cli_dataset_delete_dataset():
    id = "cii9dtexw0039uelz7nzk1lq3"

    responses.add(
        responses.DELETE,
        'https://api.mapbox.com/datasets/v1/{0}/{1}?access_token={2}'.format(username, id, access_token),
        match_querystring=True,
        status=204
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'delete-dataset', id])

    assert result.exit_code == 0

@responses.activate
def test_cli_dataset_list_features_stdout():
    id = "cii9dtexw0039uelz7nzk1lq3"
    collection='{"type":"FeatureCollection","features":[]}'
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(username, id, access_token),
        match_querystring=True,
        status=200, body=collection,
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'list-features', id])

    assert result.exit_code == 0
    assert result.output.strip() == collection.strip()

@responses.activate
def test_cli_dataset_list_features_pagination():
    id = "cii9dtexw0039uelz7nzk1lq3"
    collection='{"type":"FeatureCollection","features":[]}'
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/dataset-1/features'.format(username),
        match_querystring=False,
        status=200, body=collection,
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'list-features', 'dataset-1',
         '--start', id,
         '--limit', '1',
         '--reverse', True])

    url = responses.calls[0].request.url
    assert re.search('start=cii9dtexw0039uelz7nzk1lq3', url) != None
    assert re.search('limit=1', url) != None
    assert re.search('reverse=true', url) != None
    assert result.exit_code == 0

@responses.activate
def test_cli_dataset_list_features_tofile(tmpdir):
    tmpfile=str(tmpdir.join('test.list-features.json'))
    id = "dataset-1"
    collection='{"type":"FeatureCollection","features":[]}'
    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(username, id, access_token),
        match_querystring=True,
        status=200, body=collection,
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'list-features', id,
         '--output', tmpfile])

    assert result.exit_code == 0
    assert result.output.strip() == ""
    assert open(tmpfile).read().strip() == collection.strip()

@responses.activate
def test_cli_dataset_read_feature_stdout():
    dataset = "cii9dtexw0039uelz7nzk1lq3"
    id = "abc"
    feature = """
        {{
          "type":"Feature",
          "id":"{0}",
          "properties":{{}},
          "geometry":{{"type":"Point","coordinates":[0,0]}}
        }}""".format(id)

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features/{2}?access_token={3}'.format(username, dataset, id, access_token),
        match_querystring=True,
        status=200, body=feature,
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'read-feature', dataset, id])

    assert result.exit_code == 0
    assert result.output.strip() == feature.strip()

@responses.activate
def test_cli_dataset_read_feature_tofile(tmpdir):
    tmpfile = str(tmpdir.join('test.read-feature.json'))
    dataset = "dataset-2"
    id = "abc"
    feature = """
        {{
          "type":"Feature",
          "id":"{0}",
          "properties":{{}},
          "geometry":{{"type":"Point","coordinates":[0,0]}}
        }}""".format(id)

    responses.add(
        responses.GET,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features/{2}?access_token={3}'.format(username, dataset, id, access_token),
        match_querystring=True,
        status=200, body=feature,
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'read-feature', dataset, id,
         '--output', tmpfile])

    assert result.exit_code == 0
    assert result.output.strip() == ""
    assert open(tmpfile).read().strip() == feature.strip()

@responses.activate
def test_cli_dataset_put_feature_inline():
    dataset = "dataset-2"
    id = "abc"

    feature = """
        {{
          "type":"Feature",
          "id":"{0}",
          "properties":{{}},
          "geometry":{{"type":"Point","coordinates":[0,0]}}
        }}""".format(id)

    feature = "".join(feature.split())

    responses.add(
        responses.PUT,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features/{2}?access_token={3}'.format(username, dataset, id, access_token),
        match_querystring=True,
        status=200, body=feature,
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'put-feature', dataset, id, feature])

    assert result.exit_code == 0
    assert result.output.strip() == feature.strip()

@responses.activate
def test_cli_dataset_put_feature_fromfile(tmpdir):
    tmpfile = str(tmpdir.join('test.put-feature.json'))
    dataset = "dataset-2"
    id = "abc"

    feature = """
        {{
          "type":"Feature",
          "id":"{0}",
          "properties":{{}},
          "geometry":{{"type":"Point","coordinates":[0,0]}}
        }}""".format(id)

    feature = "".join(feature.split())

    f = open(tmpfile, 'w')
    f.write(feature)
    f.close()

    responses.add(
        responses.PUT,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features/{2}?access_token={3}'.format(username, dataset, id, access_token),
        match_querystring=True,
        status=200, body=feature,
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'put-feature', dataset, id,
         '--input', tmpfile])

    assert result.exit_code == 0
    assert result.output.strip() == feature.strip()

@responses.activate
def test_cli_dataset_put_feature_stdin():
    dataset = "dataset-2"
    id = "abc"

    feature = """
        {{
          "type":"Feature",
          "id":"{0}",
          "properties":{{}},
          "geometry":{{"type":"Point","coordinates":[0,0]}}
        }}""".format(id)

    feature = "".join(feature.split())

    responses.add(
        responses.PUT,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features/{2}?access_token={3}'.format(username, dataset, id, access_token),
        match_querystring=True,
        status=200, body=feature,
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'put-feature', dataset, id],
        input=feature)

    assert result.exit_code == 0
    assert result.output.strip() == feature.strip()

@responses.activate
def test_cli_dataset_delete_feature():
    dataset = "dataset-2"
    id = "abc"

    responses.add(
        responses.DELETE,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features/{2}?access_token={3}'.format(username, dataset, id, access_token),
        match_querystring=True,
        status=204
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'delete-feature', dataset, id])

    assert result.exit_code == 0

@responses.activate
def test_cli_dataset_batch_update_feature_inline():
    dataset = "dataset-3"
    puts = """
    [
      {"type":"Feature","id":"a","properties":{},"geometry":{"type":"Point","coordinates":[0,0]}},
      {"type":"Feature","id":"b","properties":{},"geometry":{"type":"Point","coordinates":[1,1]}}
    ]
    """
    deletes = '["c"]'
    puts = "".join(puts.split())
    expected='{{"put":{0},"delete":{1}}}'.format(puts, deletes)

    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(username, dataset, access_token),
        status=200, body=expected,
        match_querystring=True,
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'batch-update-features', dataset, puts, deletes])

    assert result.exit_code == 0
    assert result.output.strip() == expected

@responses.activate
def test_cli_dataset_batch_update_feature_fromfile(tmpdir):
    tmpfile = str(tmpdir.join('test.batch-update-features.json'))
    dataset = "dataset-3"
    puts = """
    [
      {"type":"Feature","id":"a","properties":{},"geometry":{"type":"Point","coordinates":[0,0]}},
      {"type":"Feature","id":"b","properties":{},"geometry":{"type":"Point","coordinates":[1,1]}}
    ]
    """
    deletes='["c"]'
    puts = "".join(puts.split())
    expected='{{"put":{0},"delete":{1}}}'.format(puts, deletes)

    f = open(tmpfile, 'w')
    f.write(expected)
    f.close()

    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(username, dataset, access_token),
        status=200, body=expected,
        match_querystring=True,
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'batch-update-features', dataset,
         '--input', tmpfile])

    assert result.exit_code == 0
    assert result.output.strip() == expected

@responses.activate
def test_cli_dataset_batch_update_feature_stdin():
    dataset = "dataset-3"
    puts = """
    [
      {"type":"Feature","id":"a","properties":{},"geometry":{"type":"Point","coordinates":[0,0]}},
      {"type":"Feature","id":"b","properties":{},"geometry":{"type":"Point","coordinates":[1,1]}}
    ]
    """
    deletes='["c"]'
    puts = "".join(puts.split())
    expected='{{"put":{0},"delete":{1}}}'.format(puts, deletes)

    responses.add(
        responses.POST,
        'https://api.mapbox.com/datasets/v1/{0}/{1}/features?access_token={2}'.format(username, dataset, access_token),
        status=200, body=expected,
        match_querystring=True,
        content_type='application/json'
    )

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'datasets',
         'batch-update-features', dataset],
        input=expected)

    assert result.exit_code == 0
    assert result.output.strip() == expected

@responses.activate
def test_cli_dataset_create_tileset():
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
        'https://api.mapbox.com/uploads/v1/{0}?access_token={1}'.format(owner, access_token),
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
