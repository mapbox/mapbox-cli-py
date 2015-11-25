# mapbox-cli-py

[![Build Status](https://travis-ci.org/mapbox/mapbox-cli-py.svg)](https://travis-ci.org/mapbox/mapbox-cli-py) [![Coverage Status](https://coveralls.io/repos/mapbox/mapbox-cli-py/badge.svg?branch=master&service=github)](https://coveralls.io/github/mapbox/mapbox-cli-py?branch=master)

Experimental command line interface to Mapbox Web Services and testbed for
https://github.com/mapbox/mapbox-sdk-py.

## Examples

Geocode locations

    $ x-mapbox geocoding "Portland, OR" | jq .features[0] > origin.json
    $ x-mapbox geocoding "Bend, OR" | jq .features[0] > destination.json

Get driving directions

    $ x-mapbox directions --geojson origin.json destination.json > routes.geojson

Get distance matrix

    $ x-mapbox distances origin.json destination.json > matrix.json

Get surface values
    
    $ x-mapbox surface mapbox.mapbox-terrain-v1 contour ele "[-122.781, 45.528]" "[-122.716, 45.525]"

Upload datasets

    $ x-mapbox upload username.route routes.geojson
