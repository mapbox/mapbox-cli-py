# Geocoder

CLI for the [Geocoding API](https://www.mapbox.com/developers/api/geocoding/)

The ``mbx-geocode`` command can do forward or reverse geocoding.

- Forward (place names ⇢ longitude, latitude)
- Reverse (longitude, latitude ⇢ place names)

## Usage

```
$ mbx geocode --help
Usage: mbx geocode [OPTIONS] [QUERY]

    This command returns places matching an address (forward mode) or places
    matching coordinates (reverse mode).

    In forward (the default) mode the query argument shall be an address such
    as '1600 pennsylvania ave nw'.

    $ mbx geocode '1600 pennsylvania ave nw'

    In reverse mode the query argument shall be a JSON encoded array of
    longitude and latitude (in that order) in decimal degrees.

    $ mbx geocode --reverse '[-77.4371, 37.5227]'

    An access token is required, see `mbx --help`.

Options:
    --forward / --reverse  Perform a forward or reverse geocode. [default:
                            forward]
    -i, --include          Include HTTP headers in the output.
    --lat FLOAT            Bias results toward this latitude (decimal degrees).
                            --lon is also required.
    --lon FLOAT            Bias results toward this longitude (decimal degrees).
                            --lat is also required.
    -t, --place-type NAME  Restrict results to one or more of these place types:
                            ['address', 'country', 'place', 'poi', 'postcode',
                            'region'].
    -o, --output TEXT      Save output to a file.
    --help                 Show this message and exit.
```

Its output can be piped to [geojsonio](http://geojson.io) using
[geojsonio-cli](https://github.com/mapbox/geojsonio-cli>)

    $ mbx geocode 'Chester, NJ' | geojsonio

