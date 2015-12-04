import json

import pytest

from mapboxcli.scripts.helpers import (coords_from_query, iter_query,
                                       normalize_waypoints)


def test_iter_query_string():
    assert iter_query("lolwut") == ["lolwut"]


def test_iter_query_file(tmpdir):
    filename = str(tmpdir.join('test.txt'))
    with open(filename, 'w') as f:
        f.write("lolwut")
    assert iter_query(filename) == ["lolwut"]


def test_coords_from_query_json():
    assert coords_from_query("[-100, 40]") == (-100, 40)


def test_coords_from_query_csv():
    assert coords_from_query("-100, 40") == (-100, 40)


def test_coords_from_query_ws():
    assert coords_from_query("-100 40") == (-100, 40)


@pytest.fixture
def expected_waypoints():
    with open("tests/twopoints.geojson") as src:
        fc = json.loads(src.read())
        return fc['features']


def _geoms(features):
    for feature in features:
        return feature['geometry']


def test_featurecollection_file(expected_waypoints):
    features = normalize_waypoints(["tests/twopoints.geojson"])
    assert _geoms(features) == _geoms(expected_waypoints)


def test_featuresequence(expected_waypoints):
    features = normalize_waypoints(["tests/twopoints_seq.geojson"])
    assert _geoms(features) == _geoms(expected_waypoints)


def test_featuresequencers(expected_waypoints):
    features = normalize_waypoints(["tests/twopoints_seqrs.geojson"])
    assert _geoms(features) == _geoms(expected_waypoints)


def test_coordarrays(expected_waypoints):
    inputs = ["[-122.7282, 45.5801]", "[-121.3153, 44.0582]"]
    features = normalize_waypoints(inputs)
    assert _geoms(features) == _geoms(expected_waypoints)


def test_coordpairs_comma(expected_waypoints):
    inputs = ["-122.7282, 45.5801", "-121.3153, 44.0582"]
    features = normalize_waypoints(inputs)
    assert _geoms(features) == _geoms(expected_waypoints)


def test_coordpairs_space(expected_waypoints):
    inputs = ["-122.7282 45.5801", "-121.3153 44.0582"]
    features = normalize_waypoints(inputs)
    assert _geoms(features) == _geoms(expected_waypoints)
