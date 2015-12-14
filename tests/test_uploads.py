import base64

from click.testing import CliRunner
import responses

from mapboxcli.scripts.cli import main_group
import mapbox


username = 'testuser'
access_token = 'pk.{0}.test'.format(
    base64.b64encode(b'{"u":"testuser"}').decode('utf-8'))

upload_response_body = """
    {{"progress": 0,
    "modified": "date.test",
    "error": null,
    "tileset": "{username}.test1",
    "complete": false,
    "owner": "{username}",
    "created": "date.test",
    "id": "id.test",
    "name": null}}""".format(username=username)


class MockSession(object):
    """ Mocks a boto3 session,
    specifically for the purposes of an s3 key put
    """
    def __init__(self, *args, **kwargs):
        self.bucket = None
        self.key = None
        pass

    def resource(self, name):
        self.resource_name = name
        return self

    def Object(self, bucket, key):
        assert self.resource_name == 's3'
        self.bucket = bucket
        self.key = key
        return self

    def put(self, Body):
        assert self.bucket
        assert self.key
        self.body = Body
        return True


@responses.activate
def test_cli_upload(monkeypatch):

    monkeypatch.setattr(mapbox.services.uploads, 'boto3_session', MockSession)

    # Credentials
    query_body = """
       {{"key": "_pending/{username}/key.test",
         "accessKeyId": "ak.test",
         "bucket": "tilestream-tilesets-production",
         "url": "https://tilestream-tilesets-production.s3.amazonaws.com/_pending/{username}/key.test",
         "secretAccessKey": "sak.test",
         "sessionToken": "st.test"}}""".format(username=username)

    responses.add(
        responses.GET,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body=query_body, status=200,
        content_type='application/json')

    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body=upload_response_body, status=201,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'upload',
         'test-data',
         'tests/twopoints.geojson'])
    assert result.exit_code == 0


@responses.activate
def test_cli_upload_unknown_error(monkeypatch):

    monkeypatch.setattr(mapbox.services.uploads, 'boto3_session', MockSession)

    # Credentials
    query_body = """
       {{"key": "_pending/{username}/key.test",
         "accessKeyId": "ak.test",
         "bucket": "tilestream-tilesets-production",
         "url": "https://tilestream-tilesets-production.s3.amazonaws.com/_pending/{username}/key.test",
         "secretAccessKey": "sak.test",
         "sessionToken": "st.test"}}""".format(username=username)

    responses.add(
        responses.GET,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body=query_body, status=200,
        content_type='application/json')

    responses.add(
        responses.POST,
        'https://api.mapbox.com/uploads/v1/{0}?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body='{"message":"Something went wrong"}', status=500,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'upload',
         'test-data',
         'tests/twopoints.geojson'])
    assert result.exit_code == 1
    assert result.output == 'Error: {"message":"Something went wrong"}\n'

@responses.activate
def test_cli_upload_doesnotexist(monkeypatch):

    monkeypatch.setattr(mapbox.services.uploads, 'boto3_session', MockSession)

    # Credentials
    query_body = """
       {{"key": "_pending/{username}/key.test",
         "accessKeyId": "ak.test",
         "bucket": "tilestream-tilesets-production",
         "url": "https://tilestream-tilesets-production.s3.amazonaws.com/_pending/{username}/key.test",
         "secretAccessKey": "sak.test",
         "sessionToken": "st.test"}}""".format(username=username)

    responses.add(
        responses.GET,
        'https://api.mapbox.com/uploads/v1/{0}/credentials?access_token={1}'.format(username, access_token),
        match_querystring=True,
        body=query_body, status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', access_token,
         'upload',
         'test-data',
         'tests/doesnotexist.gml'])
    assert result.exit_code == 2
