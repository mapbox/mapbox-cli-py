from click.testing import CliRunner

from mapboxcli.scripts.cli import main_group


def test_config_file(tmpdir):
    """Get options from a config file."""
    config = str(tmpdir.join('mapbox.ini'))
    with open(config, 'w') as cfg:
        cfg.write("[mapbox]\n")
        cfg.write("access-token = pk.test_config_file\n")
        cfg.write("verbosity = 11\n")
    runner = CliRunner()
    result = runner.invoke(main_group, ['-c', config, 'config'], catch_exceptions=False)
    assert config in result.output
    assert "access-token = pk.test_config_file" in result.output
    assert "verbosity = 11" in result.output


def test_config_options():
    """Get options from command line."""
    runner = CliRunner()
    result = runner.invoke(
        main_group,
        ['--access-token', 'pk.test_config_options', '-vvvv', '-q', 'config'],
        catch_exceptions=False)
    assert "Config file" not in result.output
    assert "access-token = pk.test_config_options" in result.output
    assert "verbosity = 3" in result.output


def test_config_envvar(monkeypatch):
    """Get access token from MAPBOX_ACCESS_TOKEN."""
    monkeypatch.setenv('MAPBOX_ACCESS_TOKEN', 'pk.test_config_envvar_2')
    runner = CliRunner()
    result = runner.invoke(main_group, ['config'], catch_exceptions=False)
    assert "Config file" not in result.output
    assert "access-token = pk.test_config_envvar_2" in result.output
    assert "MAPBOX_ACCESS_TOKEN = pk.test_config_envvar_2" in result.output
    monkeypatch.undo()


def test_config_envvar_2(monkeypatch):
    """Get access token from MapboxAccessToken."""
    monkeypatch.setenv('MapboxAccessToken', 'pk.test_config_envvar_2')
    monkeypatch.delenv('MAPBOX_ACCESS_TOKEN', raising=False)
    runner = CliRunner()
    result = runner.invoke(main_group, ['config'], catch_exceptions=False)
    assert "Config file" not in result.output
    assert "MapboxAccessToken = pk.test_config_envvar_2" in result.output
    assert "access-token = pk.test_config_envvar_2" in result.output
    monkeypatch.undo()


def test_config_envvar_verbosity(monkeypatch):
    """Get verbosity from MAPBOX_VERBOSE."""
    monkeypatch.setenv('MAPBOX_VERBOSE', '11')
    runner = CliRunner()
    result = runner.invoke(main_group, ['config'], catch_exceptions=False)
    assert "Config file" not in result.output
    assert "verbosity = 11" in result.output
    assert "MAPBOX_VERBOSE = 11" in result.output
    monkeypatch.undo()
