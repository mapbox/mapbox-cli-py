from os import (
    remove,
    stat
)

from mapboxcli.scripts.cli import main_group

from click.testing import CliRunner

import responses


# mapbox maps tile

def test_cli_maps_tile_error_no_column():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--row", "0",
            "--zoom-level", "0",
            "mapbox.streets",
            "0.png"
        ]
    )

    assert result.exit_code != 1
    assert "Error" in result.output


def test_cli_maps_tile_error_no_row():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--zoom-level", "0",
            "mapbox.streets",
            "0.png"
        ]
    )

    assert result.exit_code != 1
    assert "Error" in result.output


def test_cli_maps_tile_errow_no_zoom():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "0",
            "mapbox.streets",
            "0.png"
        ]
    )

    assert result.exit_code != 1
    assert "Error" in result.output


def test_cli_maps_tile_error_no_map_id():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "0",
            "--zoom-level", "0",
            "0.png"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output 


def test_cli_maps_tile_error_no_output():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "0",
            "--zoom-level", "0",
            "mapbox.streets"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


def test_cli_maps_tile_validation_error():
    # invalid --column

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "-1",
            "--row", "0",
            "--zoom-level", "0",
            "mapbox.streets",
            "0.png"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output

    # invalid --row

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "-1",
            "--zoom-level", "0",
            "mapbox.streets",
            "0.png"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output

    # invalid --zoom-level

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "0",
            "--zoom-level", "-1",
            "mapbox.streets",
            "0.png"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


@responses.activate
def test_cli_maps_tile_server_error():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/0/0/0.png" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"0.png",
        status=500
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "0",
            "--zoom-level", "0",
            "mapbox.streets",
            "0.png"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


@responses.activate
def test_cli_maps_tile():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/0/0/0.png" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"0.png",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "0",
            "--zoom-level", "0",
            "mapbox.streets",
            "0.png"
        ]
    )

    assert result.exit_code == 0
    assert stat("0.png")
    remove("0.png")


@responses.activate
def test_cli_maps_tile_with_retina():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/0/0/0@2x.png" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"0@2x.png",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "0",
            "--zoom-level", "0",
            "--retina",
            "mapbox.streets",
            "0@2x.png"
        ]
    )

    assert result.exit_code == 0
    assert stat("0@2x.png")
    remove("0@2x.png")


@responses.activate
def test_cli_maps_tile_with_different_file_format():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/0/0/0.grid.json" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"0.grid.json",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "0",
            "--zoom-level", "0",
            "--file-format", "grid.json",
            "mapbox.streets",
            "0.grid.json"
        ]
    )

    assert result.exit_code == 0
    assert stat("0.grid.json")
    remove("0.grid.json")


@responses.activate
def test_cli_maps_tile_with_retina_and_different_file_format():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/0/0/0@2x.grid.json" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"0@2x.grid.json",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "0",
            "--zoom-level", "0",
            "--retina",
            "--file-format", "grid.json",
            "mapbox.streets",
            "0@2x.grid.json"
        ]
    )

    assert result.exit_code == 0
    assert stat("0@2x.grid.json")
    remove("0@2x.grid.json")


@responses.activate
def test_cli_maps_tile_with_style():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/0/0/0.png" +
        "?access_token=pk.test" +
        "&style=mapbox://styles/mapbox/streets-v10@2018-01-01T00:00:00.000Z",
        match_querystring=True,
        body=b"0.png",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [ 
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "0",
            "--zoom-level", "0",
            "--style-id", "mapbox://styles/mapbox/streets-v10",
            "--timestamp", "2018-01-01T00:00:00.000Z",
            "mapbox.streets",
            "0.png"
        ]
    )

    assert result.exit_code == 0
    assert stat("0.png")
    remove("0.png")


@responses.activate
def test_cli_maps_tile_with_style_and_retina():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/0/0/0@2x.png" +
        "?access_token=pk.test" +
        "&style=mapbox://styles/mapbox/streets-v10@2018-01-01T00:00:00.000Z",
        match_querystring=True,
        body=b"0@2x.png",
        status=200
    )

    runner = CliRunner()
 
    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "0",
            "--zoom-level", "0",
            "--retina",
            "--style-id", "mapbox://styles/mapbox/streets-v10",
            "--timestamp", "2018-01-01T00:00:00.000Z",
            "mapbox.streets",
            "0@2x.png"
        ]
    )

    assert result.exit_code == 0
    assert stat("0@2x.png")
    remove("0@2x.png")


@responses.activate
def test_cli_maps_tile_with_style_and_different_file_format():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/0/0/0.grid.json" +
        "?access_token=pk.test" +
        "&style=mapbox://styles/mapbox/streets-v10@2018-01-01T00:00:00.000Z",
        match_querystring=True,
        body=b"0.grid.json",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [ 
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "0",
            "--zoom-level", "0",
            "--file-format", "grid.json",
            "--style-id", "mapbox://styles/mapbox/streets-v10",
            "--timestamp", "2018-01-01T00:00:00.000Z",
            "mapbox.streets",
            "0.grid.json"
        ]
    )

    assert result.exit_code == 0
    assert stat("0.grid.json")
    remove("0.grid.json")


@responses.activate
def test_cli_maps_tile_with_style_and_retina_and_different_file_format():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/0/0/0@2x.grid.json" +
        "?access_token=pk.test" +
        "&style=mapbox://styles/mapbox/streets-v10@2018-01-01T00:00:00.000Z",
        match_querystring=True,
        body=b"0@2x.grid.json",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "--column", "0",
            "--row", "0",
            "--zoom-level", "0",
            "--retina",
            "--file-format", "grid.json",
            "--style-id", "mapbox://styles/mapbox/streets-v10",
            "--timestamp", "2018-01-01T00:00:00.000Z",
            "mapbox.streets",
            "0@2x.grid.json"
        ]
    )

    assert result.exit_code == 0
    assert stat("0@2x.grid.json")
    remove("0@2x.grid.json")


@responses.activate
def test_cli_maps_tile_with_short_options():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/0/0/0@2x.grid.json" +
        "?access_token=pk.test" +
        "&style=mapbox://styles/mapbox/streets-v10@2018-01-01T00:00:00.000Z",
        match_querystring=True,
        body=b"0@2x.grid.json",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "tile",
            "-x", "0",
            "-y", "0",
            "-z", "0",
            "--retina",
            "-f", "grid.json",
            "-s", "mapbox://styles/mapbox/streets-v10",
            "-t", "2018-01-01T00:00:00.000Z",
            "mapbox.streets",
            "0@2x.grid.json"
        ]
    )

    assert result.exit_code == 0
    assert stat("0@2x.grid.json")
    remove("0@2x.grid.json")


# mapbox maps features

def test_cli_maps_features_error_no_map_id():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "features"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


def test_cli_maps_features_validation_error():
    # invalid --format

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "features",
            "--feature-format", "invalid",
            "mapbox.streets"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


@responses.activate
def test_cli_maps_features_server_error():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/features.json" +
        "?access_token=pk.test",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=500
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "features",
            "mapbox.streets"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


@responses.activate
def test_cli_maps_features():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/features.json" +
        "?access_token=pk.test",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "features",
            "mapbox.streets"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_maps_features_with_different_feature_format():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/features.kml" +
        "?access_token=pk.test",
        match_querystring=True,
        body="<xml></xml>",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "features",
            "--feature-format", "kml",
            "mapbox.streets"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "<xml></xml>" + "\n"


@responses.activate
def test_cli_maps_features_with_output():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/features.json" +
        "?access_token=pk.test",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "features",
            "mapbox.streets",
            "features.json"
        ]
    )

    assert result.exit_code == 0
    assert stat("features.json")
    remove("features.json")


@responses.activate
def test_cli_maps_features_with_different_feature_format_and_output():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/features.kml" +
        "?access_token=pk.test",
        match_querystring=True,
        body="<xml></xml>",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "features",
            "--feature-format", "kml",
            "mapbox.streets",
            "features.kml"
        ]
    )

    assert result.exit_code == 0
    assert stat("features.kml")
    remove("features.kml")


@responses.activate
def test_cli_maps_features_with_short_options():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets" +
        "/features.kml" +
        "?access_token=pk.test",
        match_querystring=True,
        body="<xml></xml>",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "features",
            "-f", "kml",
            "mapbox.streets",
            "features.kml"
        ]
    )

    assert result.exit_code == 0
    assert stat("features.kml")
    remove("features.kml")


# mapbox maps metadata

def test_cli_maps_metadata_error_no_map_id():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "metadata"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


@responses.activate
def test_cli_maps_metadata_server_error():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets.json" +
        "?access_token=pk.test",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=500
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "metadata",
            "mapbox.streets"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


@responses.activate
def test_cli_maps_metadata():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets.json" +
        "?access_token=pk.test",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "metadata",
            "mapbox.streets"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_maps_metadata_with_secure():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets.json" +
        "?access_token=pk.test" +
        "&secure",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "metadata",
            "--secure",
            "mapbox.streets"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_maps_metadata_with_output():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets.json" +
        "?access_token=pk.test",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "metadata",
            "mapbox.streets",
            "mapbox.streets.json"
        ]
    )

    assert result.exit_code == 0
    assert stat("mapbox.streets.json")
    remove("mapbox.streets.json")


@responses.activate
def test_cli_maps_metadata_with_secure_and_output():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4" +
        "/mapbox.streets.json" +
        "?access_token=pk.test" +
        "&secure",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "metadata",
            "mapbox.streets",
            "mapbox.streets.json"
        ]
    )

    assert result.exit_code == 0
    assert stat("mapbox.streets.json")
    remove("mapbox.streets.json")


# mapbox maps marker

def test_cli_maps_marker_error_no_marker_name():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "pin-s.png"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


def test_cli_maps_marker_error_no_output():
    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "--marker-name", "pin-s"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


def test_cli_maps_marker_validation_error():
    # invalid --marker-name

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "--marker-name", "invalid",
            "pin-s.png"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output

    # invalid --color

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "--marker-name", "pin-s",
            "--color", "invalid",
            "pin-s.png"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output

    # invalid --label

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "--marker-name", "pin-s",
            "--label", "invalid_",
            "pin-s.png"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


@responses.activate
def test_cli_maps_marker_server_error():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4/marker" +
        "/pin-s.png" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"pin-s.png",
        status=500
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "--marker-name", "pin-s",
            "pin-s.png"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


@responses.activate
def test_cli_maps_marker():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4/marker" +
        "/pin-s.png" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"pin-s.png",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "--marker-name", "pin-s",
            "pin-s.png"
        ]
    )

    assert result.exit_code == 0
    assert stat("pin-s.png")
    remove("pin-s.png")


@responses.activate
def test_cli_maps_marker_with_label():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4/marker" +
        "/pin-s-label.png" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"pin-s-label.png",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "--marker-name", "pin-s",
            "--label", "label",
            "pin-s-label.png"
        ]
    )

    assert result.exit_code == 0
    assert stat("pin-s-label.png")
    remove("pin-s-label.png")


@responses.activate
def test_cli_maps_marker_with_color():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4/marker" +
        "/pin-s+00f.png" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"pin-s+00f.png",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "--marker-name", "pin-s",
            "--color", "00f",
            "pin-s+00f.png"
        ]
    )

    assert result.exit_code == 0
    assert stat("pin-s+00f.png")
    remove("pin-s+00f.png")


@responses.activate
def test_cli_maps_marker_with_retina():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4/marker" +
        "/pin-s@2x.png" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"pin-s@2x.png",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "--marker-name", "pin-s",
            "--retina",
            "pin-s@2x.png"
        ]
    )

    assert result.exit_code == 0
    assert stat("pin-s@2x.png")
    remove("pin-s@2x.png")


@responses.activate
def test_cli_maps_marker_with_label_and_color():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4/marker" +
        "/pin-s-label+00f.png" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"pin-s-label+00f.png",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "--marker-name", "pin-s",
            "--label", "label",
            "--color", "00f",
            "pin-s-label+00f.png"
        ]
    )

    assert result.exit_code == 0
    assert stat("pin-s-label+00f.png")
    remove("pin-s-label+00f.png")


@responses.activate
def test_cli_maps_marker_with_color_and_retina():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4/marker/pin-s+00f@2x.png" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"pin-s+00f@2x.png",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "--marker-name", "pin-s",
            "--color", "00f",
            "--retina",
            "pin-s+00f@2x.png"
        ]
    )

    assert result.exit_code == 0
    assert stat("pin-s+00f@2x.png")
    remove("pin-s+00f@2x.png")


@responses.activate
def test_cli_maps_marker_with_label_and_retina():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4/marker" +
        "/pin-s-label@2x.png" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"pin-s-label@2x.png",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "--marker-name", "pin-s",
            "--label", "label",
            "--retina",
            "pin-s-label@2x.png"
        ]
    )

    assert result.exit_code == 0
    assert stat("pin-s-label@2x.png")
    remove("pin-s-label@2x.png")


@responses.activate
def test_cli_maps_marker_with_label_and_color_and_retina():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4/marker" +
        "/pin-s-label+00f@2x.png" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"pin-s-label+00f@2x.png",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "--marker-name", "pin-s",
            "--label", "label",
            "--color", "00f",
            "--retina",
            "pin-s-label+00f@2x.png"
        ]
    )

    assert result.exit_code == 0
    assert stat("pin-s-label+00f@2x.png")
    remove("pin-s-label+00f@2x.png")


@responses.activate
def test_cli_maps_marker_with_short_options():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
        "/v4/marker" +
        "/pin-s-label+00f@2x.png" +
        "?access_token=pk.test",
        match_querystring=True,
        body=b"pin-s-label+00f@2x.png",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "pk.test",
            "maps", "marker",
            "-m", "pin-s",
            "-l", "label",
            "-c", "00f",
            "--retina",
            "pin-s-label+00f@2x.png"
        ]
    )

    assert result.exit_code == 0
    assert stat("pin-s-label+00f@2x.png")
    remove("pin-s-label+00f@2x.png")
