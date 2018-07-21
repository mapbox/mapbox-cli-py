from os import (
    remove,
    stat
)

from mapboxcli.scripts.cli import main_group

from click.testing import CliRunner

from pytest import mark

from responses import (
    activate,
    add,
    GET
)


# test invalid value for --radius (click.IntRange)

def test_cli_tilequery_radius_invalid():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--radius", "-- -1",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


# test invalid values for --limit (click.IntRange)

@mark.parametrize("limit", ["0", "51"])
def test_cli_tilequery_limit_invalid(limit):
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--limit", limit,
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


def test_cli_tilequery_validation_error():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "mapbox.mapbox-streets-v10",
            "--",
            "-181.0",
            "1.1"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


@activate
def test_cli_tilequery_server_error():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=500
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


@activate
def test_tilequery_one_mapid():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_two_mapids():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v9%2Cmapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "mapbox.mapbox-streets-v9",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"
    
 
@activate
def test_tilequery_negative_lon():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/-0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "mapbox.mapbox-streets-v10",
            "--",
            "-0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_negative_lat():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C-1.1.json" +
        "?access_token=pk.test" +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "--",
            "-1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
@mark.parametrize("radius", ["0", "1000", "1000000"])
def test_tilequery_with_radius(radius):
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius={}".format(radius) +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--radius", radius,
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
@mark.parametrize("limit", ["1", "25", "50"])
def test_tilequery_with_limit(limit):
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&limit={}".format(limit) +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--limit", limit,
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_with_dedupe():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--dedupe",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
@mark.parametrize("geometry", ["linestring", "point", "polygon"])
def test_tilequery_with_geometry(geometry):
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&dedupe=true" +
        "&geometry={}".format(geometry),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--geometry", geometry,
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_with_layers():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&dedupe=true" +
        "&layers=layer0%2Clayer1%2Clayer2",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--layer", "layer0",
            "--layer", "layer1",
            "--layer", "layer2",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_with_output():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--output", "output.json",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert stat("output.json")
    remove("output.json")


@activate
def test_tilequery_with_radius_and_limit():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--radius", "25",
            "--limit", "25",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_with_radius_and_dedupe():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--radius", "25",
            "--dedupe",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_with_radius_and_geometry():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&dedupe=true" + 
        "&geometry=linestring",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--radius", "25",
            "--geometry", "linestring",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_with_radius_and_layers():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&dedupe=true" + 
        "&layers=layer0%2Clayer1%2Clayer2",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--radius", "25",
            "--layer", "layer0",
            "--layer", "layer1",
            "--layer", "layer2",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_with_radius_limit_and_dedupe():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&dedupe=true",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--radius", "25",
            "--limit", "25",
            "--dedupe",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_with_radius_limit_and_geometry():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&dedupe=true" + 
        "&geometry=linestring",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--radius", "25",
            "--limit", "25",
            "--geometry", "linestring",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_with_radius_limit_and_layers():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&dedupe=true" + 
        "&layers=layer0%2Clayer1%2Clayer2",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--radius", "25",
            "--limit", "25",
            "--layer", "layer0",
            "--layer", "layer1",
            "--layer", "layer2",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_with_radius_limit_dedupe_and_geometry():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&dedupe=true" +
        "&geometry=linestring",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--radius", "25",
            "--limit", "25",
            "--dedupe",
            "--geometry", "linestring",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_with_radius_limit_dedupe_and_layers():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&dedupe=true" +
        "&layers=layer0%2Clayer1%2Clayer2",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--radius", "25",
            "--limit", "25",
            "--dedupe",
            "--layer", "layer0",
            "--layer", "layer1",
            "--layer", "layer2",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_with_radius_limit_dedupe_geometry_and_layers():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&dedupe=true" +
        "&geometry=linestring" +
        "&layers=layer0%2Clayer1%2Clayer2",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--radius", "25",
            "--limit", "25",
            "--dedupe",
            "--geometry", "linestring",
            "--layer", "layer0",
            "--layer", "layer1",
            "--layer", "layer2",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@activate
def test_tilequery_with_radius_limit_dedupe_geometry_layers_and_output():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&dedupe=true" +
        "&geometry=linestring" +
        "&layers=layer0%2Clayer1%2Clayer2",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "--radius", "25",
            "--limit", "25",
            "--dedupe",
            "--geometry", "linestring",
            "--layer", "layer0",
            "--layer", "layer1",
            "--layer", "layer2",
            "--output", "output.json",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert stat("output.json")
    remove("output.json")


@activate
def test_cli_tilequery_short_options():
    add(
        method=GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.mapbox-streets-v10" +
        "/tilequery" +
        "/0.0%2C1.1.json" +
        "?access_token=pk.test" +
        "&radius=25" +
        "&limit=25" +
        "&dedupe=true" +
        "&geometry=linestring" +
        "&layers=layer0%2Clayer1%2Clayer2",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "tilequery",
            "-r", "25",
            "-l", "25",
            "--dedupe",
            "-g", "linestring",
            "-y", "layer0",
            "-y", "layer1",
            "-y", "layer2",
            "-o", "output.json",
            "mapbox.mapbox-streets-v10",
            "0.0",
            "1.1"
        ]
    )

    assert result.exit_code == 0
    assert stat("output.json")
    remove("output.json")
