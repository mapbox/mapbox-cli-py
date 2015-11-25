from click.testing import CliRunner
import responses
import pytest

from mapboxcli.scripts.cli import main_group


@responses.activate
@pytest.mark.skipif(True, reason="We don't have a way to mock s3 yet")
def test_cli_upload():

    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'bogus',
         'upload',
         'username.data',
         'data.geojson'])
    assert result.exit_code == 0
