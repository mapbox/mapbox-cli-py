import json

from click.testing import CliRunner
import responses

from mapboxcli.scripts.cli import main_group


@responses.activate
def test_cli_directions():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/directions/mapbox.driving/-87.337875%2C36.539157%3B-88.247681%2C36.922175.json?access_token=bogus&geometry=geojson&steps=true&alternatives=true&instructions=text',
        match_querystring=True,
        body="", status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'bogus',
         'directions',
         "[-87.33787536621092, 36.539156961321574]",
         "[-88.2476806640625, 36.92217534275667]"])
    assert result.exit_code == 0


@responses.activate
def test_cli_directions_geojson():

    with open('tests/moors.json') as fh:
        body = fh.read()

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/directions/mapbox.driving/-87.337875%2C36.539157%3B-88.247681%2C36.922175.json?access_token=bogus&geometry=geojson&steps=true&alternatives=true&instructions=text',
        match_querystring=True,
        body=body, status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'bogus',
         'directions',
         '--geojson',
         "[-87.33787536621092, 36.539156961321574]",
         "[-88.2476806640625, 36.92217534275667]"])

    assert result.exit_code == 0
    assert json.loads(result.output)['type'] == 'FeatureCollection'


def test_cli_bad_parameter():
    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'bogus',
         'directions',
         '--instructions', 'also_bogus',
         "[-87.33787536621092, 36.539156961321574]",
         "[-88.2476806640625, 36.92217534275667]"])

    assert result.exit_code == 2

@responses.activate
def test_cli_directions_unauthorized():

    responses.add(
        responses.GET,
        'https://api.mapbox.com/v4/directions/mapbox.driving/-87.337875%2C36.539157%3B-88.247681%2C36.922175.json?access_token=INVALID&geometry=geojson&steps=true&alternatives=true&instructions=text',
        match_querystring=True,
        body='{"message":"Not Authorized - Invalid Token"}', status=401,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ["--access-token", "INVALID",
         "directions",
         "[-87.33787536621092, 36.539156961321574]",
         "[-88.2476806640625, 36.92217534275667]"])
    assert result.exit_code == 1
    assert result.output == 'Error: {"message":"Not Authorized - Invalid Token"}\n'
