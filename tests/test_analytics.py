from click.testing import CliRunner
from mapboxcli.scripts.cli import main_group
import responses


mock_response_200 = responses.Response(
  method="GET",
  url="https://api.mapbox.com/analytics/v1/accounts/mapbox-user?access_token=mapbox-token&period=2018-04-15T00%3A00%3A00.000Z%2C2018-04-16T00%3A00%3A00.000Z",
  match_querystring=True,
  body="{\"key\": \"value\"}",
  status=200
)


mock_response_500 = responses.Response(
  method="GET",
  url="https://api.mapbox.com/analytics/v1/accounts/mapbox-user?access_token=mapbox-token&period=2018-04-15T00%3A00%3A00.000Z%2C2018-04-16T00%3A00%3A00.000Z",
  match_querystring=True,
  body="{\"key\": \"value\"}",
  status=500
)


@responses.activate
def test_cli_analytics_success_long_options():
  responses.add(mock_response_200)

  runner = CliRunner()

  result = runner.invoke(
    main_group,
    [
      "--access-token", "mapbox-token",
      "analytics",
      "--resource-type", "accounts",
      "--username", "mapbox-user",
      "--start", "2018-04-15T00:00:00.000Z",
      "--end", "2018-04-16T00:00:00.000Z"
    ]
  )
  
  assert result.exit_code == 0
  assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_analytics_success_short_options():
  responses.add(mock_response_200)

  runner = CliRunner()

  result = runner.invoke(
    main_group,
    [
      "--access-token", "mapbox-token",
      "analytics",
      "-t", "accounts",
      "-u", "mapbox-user",
      "-s", "2018-04-15T00:00:00.000Z",
      "-e", "2018-04-16T00:00:00.000Z"
    ]
  )
  
  assert result.exit_code == 0
  assert result.output == "{\"key\": \"value\"}" + "\n"


@responses.activate
def test_cli_analytics_error_no_resource_type_long_options():
  responses.add(mock_response_200)

  runner = CliRunner()

  result = runner.invoke(
    main_group,
    [
      "--access-token", "mapbox-token",
      "analytics",
      "--username", "mapbox-user",
      "--start", "2018-04-15T00:00:00.000Z",
      "--end", "2018-04-16T00:00:00.000Z"
    ]
  )
  
  assert result.exit_code != 0
  assert "Missing option \"--resource-type\"" in result.output


@responses.activate
def test_cli_analytics_error_no_resource_type_short_options():
  responses.add(mock_response_200)

  runner = CliRunner()

  result = runner.invoke(
    main_group,
    [
      "--access-token", "mapbox-token",
      "analytics",
      "-u", "mapbox-user",
      "-s", "2018-04-15T00:00:00.000Z",
      "-e", "2018-04-16T00:00:00.000Z"
    ]
  )
  
  assert result.exit_code != 0
  assert "Missing option \"--resource-type\"" in result.output


@responses.activate
def test_cli_analytics_error_no_username_long_options():
  responses.add(mock_response_200)

  runner = CliRunner()

  result = runner.invoke(
    main_group,
    [
      "--access-token", "mapbox-token",
      "analytics",
      "--resource-type", "accounts",
      "--start", "2018-04-15T00:00:00.000Z",
      "--end", "2018-04-16T00:00:00.000Z"
    ]
  )
  
  assert result.exit_code != 0
  assert "Missing option \"--username\"" in result.output


@responses.activate
def test_cli_analytics_error_no_username_short_options():
  responses.add(mock_response_200)

  runner = CliRunner()

  result = runner.invoke(
    main_group,
    [
      "--access-token", "mapbox-token",
      "analytics",
      "-t", "accounts",
      "-s", "2018-04-15T00:00:00.000Z",
      "-e", "2018-04-16T00:00:00.000Z"
    ]
  )
  
  assert result.exit_code != 0
  assert "Missing option \"--username\"" in result.output


@responses.activate
def test_cli_analytics_error_invalid_resource_type_long_options():
  responses.add(mock_response_200)

  runner = CliRunner()

  result = runner.invoke(
    main_group,
    [
      "--access-token", "mapbox-token",
      "analytics",
      "--resource-type", "invalid",
      "--username", "mapbox-user",
      "--start", "2018-04-15T00:00:00.000Z",
      "--end", "2018-04-16T00:00:00.000Z"
    ]
  )
  
  assert result.exit_code != 0
  assert "Invalid value for \"--resource-type\"" in result.output


@responses.activate
def test_cli_analytics_error_invalid_resource_type_short_options():
  responses.add(mock_response_200)

  runner = CliRunner()

  result = runner.invoke(
    main_group,
    [
      "--access-token", "mapbox-token",
      "analytics",
      "-t", "invalid",
      "-u", "mapbox-user",
      "-s", "2018-04-15T00:00:00.000Z",
      "-e", "2018-04-16T00:00:00.000Z"
    ]
  )
  
  assert result.exit_code != 0
  assert "Invalid value for \"--resource-type\"" in result.output


@responses.activate
def test_cli_analytics_server_error():
  responses.add(mock_response_500)

  runner = CliRunner()

  result = runner.invoke(
    main_group,
    [
      "--access-token", "mapbox-token",
      "analytics",
      "--resource-type", "accounts",
      "--username", "mapbox-user",
      "--start", "2018-04-15T00:00:00.000Z",
      "--end", "2018-04-16T00:00:00.000Z"
    ]
  )

  assert result.exit_code != 0
  assert "Error" in result.output

