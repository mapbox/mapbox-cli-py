import json

from click.testing import CliRunner
import responses

from mapboxcli.scripts.cli import main_group


@responses.activate
def test_cli_geocode_fwd():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json?access_token=bogus',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'bogus', 'geocoding', '--forward', '1600 pennsylvania ave nw'],
        catch_exceptions=False)
    print(result.output)
    print(result.exception)
    print(result.exc_info)
    assert result.exit_code == 0
    assert result.output == '{"query": ["1600", "pennsylvania", "ave", "nw"]}\n'


@responses.activate
def test_cli_geocode_fwd_env_token():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json?access_token=bogus',
        match_querystring=True,
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocoding', '--forward', '1600 pennsylvania ave nw'],
        env={'MAPBOX_ACCESS_TOKEN': 'bogus'})
    assert result.exit_code == 0
    assert result.output == '{"query": ["1600", "pennsylvania", "ave", "nw"]}\n'


@responses.activate
def test_cli_geocode_reverse():

    lon, lat = -77.4371, 37.5227
    body = json.dumps({"query": [lon, lat]})

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/{0},{1}.json?access_token=pk.test'.format(lon, lat),
        match_querystring=True,
        body=body,
        status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'pk.test', 'geocoding', '--reverse'],
        input='{0},{1}'.format(lon, lat))
    assert result.exit_code == 0
    assert result.output.strip() == body


@responses.activate
def test_cli_geocode_reverse_env_token():

    lon, lat = -77.4371, 37.5227
    body = json.dumps({"query": [lon, lat]})

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/{0},{1}.json?access_token=bogus'.format(lon, lat),
        match_querystring=True,
        body=body,
        status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocoding', '--reverse'],
        input='{0},{1}'.format(lon, lat),
        env={'MAPBOX_ACCESS_TOKEN': 'bogus'})
    assert result.exit_code == 0
    assert result.output.strip() == body


@responses.activate
def test_cli_geocode_unauthorized():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json',
        body='{"message":"Not Authorized - Invalid Token"}', status=401,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(main_group, ['geocoding', '--forward',
                                        '1600 pennsylvania ave nw'])
    assert result.exit_code == 1
    assert result.output == 'Error: {"message":"Not Authorized - Invalid Token"}\n'


@responses.activate
def test_cli_geocode_rev_unauthorized():

    lon, lat = -77.4371, 37.5227

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/{0},{1}.json'.format(lon, lat),
        body='{"message":"Not Authorized - Invalid Token"}', status=401,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocoding', '--reverse'],
        input='{0},{1}'.format(lon, lat))
    assert result.exit_code == 1
    assert result.output == 'Error: {"message":"Not Authorized - Invalid Token"}\n'


@responses.activate
def test_cli_geocode_fwd_headers():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/1600%20pennsylvania%20ave%20nw.json',
        body='{"query": ["1600", "pennsylvania", "ave", "nw"]}', status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocoding', '-i', '--forward', '1600 pennsylvania ave nw'])
    assert result.exit_code == 0
    assert result.output.startswith('Content-Type')


@responses.activate
def test_cli_geocode_rev_headers():

    lon, lat = -77.4371, 37.5227
    body = json.dumps({"query": [lon, lat]})

    responses.add(
        responses.GET,
        'https://api.mapbox.com/geocoding/v5/mapbox.places/{0},{1}.json'.format(lon, lat),
        body=body,
        status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['geocoding', '-i', '--reverse'],
        input='{0},{1}'.format(lon, lat))
    assert result.exit_code == 0
    assert result.output.startswith('Content-Type')


def test_cli_geocode_bad_place():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        ['geocoding', '-t', 'spaceship'],
        input='Millennium Falcon')
    assert result.exit_code == 2

    lon, lat = -77.4371, 37.5227
    result = runner.invoke(
        main_group,
        ['geocoding', '-t', 'spaceship', '--reverse'],
        input='{0},{1}'.format(lon, lat))
    assert result.exit_code == 2


def test_cli_geocode_bad_dataset():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        ['geocoding', '-d', 'mapbox.spaceships'],
        input='Millennium Falcon')
    assert result.exit_code == 2
    assert "Invalid value" in result.output


def test_cli_geocode_invalid_country():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        ['geocoding', '--country', 'US,Tatooine'],
        input='Millennium Falcon')
    assert result.exit_code == 2
    assert "Invalid value" in result.output
