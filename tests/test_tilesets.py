import base64

from mapboxcli.scripts.cli import main_group

from click.testing import CliRunner

import responses


USERNAME = base64.b64encode(b"{\"u\":\"user\"}").decode("utf-8")
ACCESS_TOKEN = "pk.{}.test".format(USERNAME)


def test_cli_tilesets_validation_error():
    # invalid --limit

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets",
            "--limit", 1000
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


@responses.activate
def test_cli_tilesets_server_error():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=500
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets"
        ]
    )

    assert result.exit_code != 0
    assert "Error" in result.output


@responses.activate
def test_cli_tilesets():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN),
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_tilesets_with_tileset_type():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN) +
            "&type=raster",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets",
            "--tileset-type", "raster"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_tilesets_with_visibility():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN) +
            "&visibility=private",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets",
            "--visibility", "private"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_tilesets_with_sortby():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN) +
            "&sortby=created",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets",
            "--sortby", "created"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_tilesets_with_limit():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN) +
            "&limit=500",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets",
            "--limit", "500"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_tilesets_with_tileset_type_and_visibility():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN) +
            "&type=raster" +
            "&visibility=private",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets",
            "--tileset-type", "raster",
            "--visibility", "private"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_tilesets_with_tileset_type_and_sortby():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN) +
            "&type=raster" +
            "&sortby=created",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets",
            "--tileset-type", "raster",
            "--sortby", "created"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_tilesets_with_tileset_type_and_limit():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN) +
            "&type=raster" +
            "&limit=500",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets",
            "--tileset-type", "raster",
            "--limit", "500"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_tilesets_with_visibility_and_sortby():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN) +
            "&visibility=private" +
            "&sortby=created",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets",
            "--visibility", "private",
            "--sortby", "created"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_tilesets_with_visibility_and_limit():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN) +
            "&visibility=private" +
            "&limit=500",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets",
            "--visibility", "private",
            "--limit", "500"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_tilesets_with_sortby_and_limit():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN) +
            "&sortby=created" +
            "&limit=500",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets",
            "--sortby", "created",
            "--limit", "500"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_tilesets_with_tileset_type_visibility_sortby_and_limit():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN) +
            "&type=raster" +
            "&visibility=private" +
            "&sortby=created" +
            "&limit=500",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets",
            "--tileset-type", "raster",
            "--visibility", "private",
            "--sortby", "created",
            "--limit", "500"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_tilesets_with_short_options():
    responses.add(
        method=responses.GET,
        url="https://api.mapbox.com" +
            "/tilesets/v1" +
            "/user" +
            "?access_token={}".format(ACCESS_TOKEN) +
            "&type=raster" +
            "&visibility=private" +
            "&sortby=created" +
            "&limit=500",
        match_querystring=True,
        body="{\"key\": \"value\"}",
        status=200
    )

    runner = CliRunner()

    result = runner.invoke(
        main_group,
        [
            "--access-token", "{}".format(ACCESS_TOKEN),
            "tilesets",
            "-t", "raster",
            "-v", "private",
            "-s", "created",
            "-l", "500"
        ]
    )

    assert result.exit_code == 0
    assert result.output == "{\"key\": \"value\"}" + "\n"
