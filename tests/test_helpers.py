from mapboxcli.scripts.geocoding import coords_from_query, iter_query


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
