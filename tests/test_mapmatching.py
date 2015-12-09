from click.testing import CliRunner
import responses

from mapboxcli.scripts.cli import main_group


@responses.activate
def test_cli_mapmatching():

    responses.add(
        responses.POST,
        'https://api.mapbox.com/matching/v4/mapbox.cycling.json?gps_precision=4&access_token=bogus',
        match_querystring=True,
        body="", status=200,
        content_type='application/json')

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'bogus',
         "mapmatching",
         "--gps-precision", "4",
         "--profile", "mapbox.cycling",
         "tests/line_feature.geojson"])
    assert result.exit_code == 0
