from click.testing import CliRunner
import responses

from mapboxcli.scripts.cli import main_group


@responses.activate
def test_cli_static():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/mapbox.satellite/-61.7,12.1,12/600x600.png256?access_token=bogus',
        match_querystring=True,
        body='.PNG...',
        status=200,
        content_type='image/png')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'bogus',
         'staticmap',
         '--lon', '-61.7',
         '--lat', '12.1',
         '--zoom', '12',
         'mapbox.satellite',
         '/dev/null'])

    assert result.exit_code == 0


@responses.activate
def test_cli_static_features_stdin():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/mapbox.satellite/geojson(%7B%22features%22%3A%5B%7B%22geometry%22%3A%7B%22coordinates%22%3A%5B-122.7282%2C45.5801%5D%2C%22type%22%3A%22Point%22%7D%2C%22id%22%3A%220%22%2C%22properties%22%3A%7B%7D%2C%22type%22%3A%22Feature%22%7D%2C%7B%22geometry%22%3A%7B%22coordinates%22%3A%5B-121.3153%2C44.0582%5D%2C%22type%22%3A%22Point%22%7D%2C%22id%22%3A%221%22%2C%22properties%22%3A%7B%7D%2C%22type%22%3A%22Feature%22%7D%5D%2C%22type%22%3A%22FeatureCollection%22%7D)/-61.7,12.1,12/600x600.png256?access_token=bogus',
        match_querystring=True,
        body='.PNG...',
        status=200,
        content_type='image/png')

    # alternate ordering for py26
    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/mapbox.satellite/geojson(%7B%22features%22%3A%5B%7B%22geometry%22%3A%7B%22coordinates%22%3A%5B-122.7282%2C45.580100000000002%5D%2C%22type%22%3A%22Point%22%7D%2C%22id%22%3A%220%22%2C%22properties%22%3A%7B%7D%2C%22type%22%3A%22Feature%22%7D%2C%7B%22geometry%22%3A%7B%22coordinates%22%3A%5B-121.31529999999999%2C44.058199999999999%5D%2C%22type%22%3A%22Point%22%7D%2C%22id%22%3A%221%22%2C%22properties%22%3A%7B%7D%2C%22type%22%3A%22Feature%22%7D%5D%2C%22type%22%3A%22FeatureCollection%22%7D)/-61.7,12.1,12/600x600.png256?access_token=bogus',
        match_querystring=True,
        body='.PNG...',
        status=200,
        content_type='image/png')

    with open('tests/twopoints_seq.geojson', 'r') as src:
        stdin = src.read()

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'bogus',
         'staticmap',
         '--features', '-',
         '--lon', '-61.7',
         '--lat', '12.1',
         '--zoom', '12',
         'mapbox.satellite',
         '/dev/null'],
        input=stdin)

    assert result.exit_code == 0


def test_cli_bad_size():
    with open('tests/twopoints_seq.geojson', 'r') as src:
        stdin = src.read()

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'bogus',
         'staticmap',
         '--features', '-',
         '--size', '2000', '2000',
         '--zoom', '12',
         'mapbox.satellite',
         '/dev/null'],
        input=stdin)

    assert result.exit_code == 2


@responses.activate
def test_cli_static_unauthorized():
    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/mapbox.satellite/-61.7,12.1,12/600x600.png256?access_token=INVALID',
        match_querystring=True,
        body='{"message":"Not Authorized - Invalid Token"}', status=401,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'INVALID',
         'staticmap',
         '--lon', '-61.7',
         '--lat', '12.1',
         '--zoom', '12',
         'mapbox.satellite',
         '/dev/null'])

    assert result.exit_code == 1
    assert result.output == 'Error: {"message":"Not Authorized - Invalid Token"}\n'
