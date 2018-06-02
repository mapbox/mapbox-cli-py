import os

from mapboxcli.scripts.cli import main_group
from mapboxcli.scripts.directions import waypoint_snapping_callback

from click.testing import CliRunner
import pytest
import responses


GEOJSON_BODY = "{\"routes\": []}"

NON_GEOJSON_BODY = ""

OUTPUT_FILE = "test.json"

ENCODED_COORDS = "/0.0%2C0.0%3B1.0%2C1.0.json"


def test_cli_directions_validation_error():
    # --annotations invalid

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--annotations", "invalid",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output

    # --waypoint-snapping 1.1,1,1 --waypoint-snapping 1.1,1,1

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--waypoint-snapping", "1.1,1,1",
            "--waypoint-snapping", "1.1,1,1",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code != 0

    # --waypoint-snapping 1.1 --waypoint-snapping 1.1

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--waypoint-snapping", "1.1",
            "--waypoint-snapping", "1.1",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code != 0


@responses.activate
def test_cli_directions_server_error():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=NON_GEOJSON_BODY,
        status=500
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


@responses.activate
def test_cli_directions():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0


@responses.activate
def test_cli_directions_with_profile():
    # --profile mapbox/driving-traffic

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving-traffic" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--profile", "mapbox/driving-traffic",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --profile mapbox/driving

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--profile", "mapbox/driving",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --profile mapbox/walking

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/walking" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--profile", "mapbox/walking",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --profile mapbox/cycling

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/cycling" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--profile", "mapbox/cycling",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0


@responses.activate
def test_cli_directions_with_alternatives():
    # --alternatives

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--alternatives",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --no-alternatives

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=false" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--no-alternatives",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0


@responses.activate
def test_cli_directions_with_geometries():
    # --geometries geojson

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--geometries", "geojson",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --geometries polyline

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=polyline" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=NON_GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--geometries", "polyline",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --geometries polyline6

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=polyline6" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=NON_GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--geometries", "polyline6",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0


@responses.activate
def test_cli_directions_with_overview():
    # --overview full

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&overview=full" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--overview", "full",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --overview simplified

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&overview=simplified" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--overview", "simplified",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --overview False

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&overview=false" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--overview", "False",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0


@responses.activate
def test_cli_directions_with_steps():
    # --steps

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--steps",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --no-steps

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=false" +
            "&continue_straight=false",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--no-steps",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0


@responses.activate
def test_cli_directions_with_continue_straight():
    # --continue-straight

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--continue-straight",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --no-continue-straight

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=false" +
            "&continue_straight=false",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--no-continue-straight",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0


@responses.activate
def test_cli_directions_with_waypoint_snapping():
   # --waypoint-snapping 1,1,1 --waypoint-snapping 1,1,1

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true" +
            "&bearings=1%2C1%3B1%2C1" +
            "&radiuses=1%3B1",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--waypoint-snapping", "1,1,1",
            "--waypoint-snapping", "1,1,1",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

   # --waypoint-snapping 1 --waypoint-snapping 1

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true" +
            "&radiuses=1%3B1",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--waypoint-snapping", "1",
            "--waypoint-snapping", "1",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --waypoint-snapping unlimited --waypoint-snapping unlimited

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true" +
            "&radiuses=unlimited%3Bunlimited",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--waypoint-snapping", "unlimited",
            "--waypoint-snapping", "unlimited",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --waypoint-snapping 1,1,1 --waypoint-snapping 1

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true" +
            "&bearings=1%2C1%3B" +
            "&radiuses=1%3B1",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--waypoint-snapping", "1,1,1",
            "--waypoint-snapping", "1",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --waypoint-snapping 1,1,1 --waypoint-snapping unlimited

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true" +
            "&bearings=1%2C1%3B" +
            "&radiuses=1%3Bunlimited",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--waypoint-snapping", "1,1,1",
            "--waypoint-snapping", "unlimited",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --waypoint-snapping 1 --waypoint-snapping unlimited

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true" +
            "&radiuses=1%3Bunlimited",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--waypoint-snapping", "1",
            "--waypoint-snapping", "unlimited",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0


@responses.activate
def test_cli_directions_with_annotations():
    # --annotations duration

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true" +
            "&annotations=duration",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--annotations", "duration",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --annotations distance

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true" +
            "&annotations=distance",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--annotations", "distance",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

    # --annotations speed

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true" +
            "&annotations=speed",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--annotations", "speed",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0

   # --annotations duration,distance,speed

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true" +
            "&annotations=duration%2Cdistance%2Cspeed",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--annotations", "duration,distance,speed",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0


@responses.activate
def test_cli_directions_with_language():
    # --language en

    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true" +
            "&language=en",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--language", "en",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0


@responses.activate
def test_cli_directions_stdout():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--output", "-",
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0


@responses.activate
def test_cli_directions_file_output():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com/directions/v5" +
            "/mapbox/driving" +
            ENCODED_COORDS +
            "?access_token=test-token" +
            "&alternatives=true" +
            "&geometries=geojson" +
            "&steps=true" +
            "&continue_straight=true",
        match_querystring=True,
        body=GEOJSON_BODY,
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "test-token",
            "directions",
            "--output", OUTPUT_FILE,
            "[0, 0]", "[1, 1]"
        ]
    )

    assert result.exit_code == 0
    assert os.stat(OUTPUT_FILE)
    os.remove(OUTPUT_FILE)


@pytest.mark.parametrize("input_snap,expected", [
    ("1,1,1", [(1, 1, 1)]),
    ("1", [1]),
    ("unlimited", ["unlimited"]),
])
def test_waypoint_callback(input_snap, expected):
    wpt = waypoint_snapping_callback(None, None, [input_snap])
    assert wpt == expected

    wpt = waypoint_snapping_callback(None, None, (u"1", u"unlimited"))
    assert wpt == [1, "unlimited"]
