from click.testing import CliRunner
import responses

from mapboxcli.scripts.cli import main_group


@responses.activate
def test_cli_distance():

    responses.add(
        responses.POST,
        'https://api.mapbox.com/distances/v1/mapbox/driving?access_token=bogus',
        match_querystring=True,
        body='{"durations":[[0,4977,5951],[4963,0,9349],[5881,9317,0]]}',
        status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'bogus',
         'distance',
         "[-87.337875, 36.539156]",
         "[-86.577791, 36.722137]",
         "[-88.247685, 36.922175]"])
    assert result.exit_code == 0


def test_cli_distance_bad_profile():
    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'bogus',
         'distance',
         '--profile', 'segway',
         "[-87.337875, 36.539156]",
         "[-86.577791, 36.722137]",
         "[-88.247685, 36.922175]"])
    assert result.exit_code == 2


@responses.activate
def test_cli_distance_invalid_token():

    responses.add(
        responses.POST,
        'https://api.mapbox.com/distances/v1/mapbox/driving?access_token=INVALID',
        match_querystring=True,
        body='{"message":"Not Authorized - Invalid Token"}', status=401,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'INVALID',
         'distance',
         "[-87.337875, 36.539156]",
         "[-86.577791, 36.722137]",
         "[-88.247685, 36.922175]"])
    assert result.exit_code == 1
    assert result.output == 'Error: {"message":"Not Authorized - Invalid Token"}\n'
