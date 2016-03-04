import base64
import json

from click.testing import CliRunner
import responses

from mapboxcli.scripts.cli import main_group
import mapbox

username = 'testuser'
access_token = 'sk.{0}.test'.format(
    base64.b64encode(b'{"u":"testuser"}').decode('utf-8'))


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