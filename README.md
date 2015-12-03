# mapbox-cli-py

[![Build Status](https://travis-ci.org/mapbox/mapbox-cli-py.svg?branch=master)](https://travis-ci.org/mapbox/mapbox-cli-py) [![Coverage Status](https://coveralls.io/repos/mapbox/mapbox-cli-py/badge.svg?branch=master&service=github)](https://coveralls.io/github/mapbox/mapbox-cli-py?branch=master)

Experimental command line interface to Mapbox Web Services and testbed for
https://github.com/mapbox/mapbox-sdk-py.

## Installation

```
git checkout git@github.com:mapbox/mapbox-cli-py.git
cd mapbox-cli-py
pip install -e .[test]
```

## Usage

* [directions](#directions)
* [distance](#distance)
* [geocoding](#geocoding)
* [staticmap](#staticmap)
* [surface](#surface)
* [upload](#upload)

### directions
```
Usage: x-mapbox directions [OPTIONS] [WAYPOINTS]...

  Calculate optimal route with turn-by-turn directions between up to 25
  waypoints.

    $ x-mapbox directions "[-122.681032, 45.528334]" "[-122.71679,
    45.525135]"

  An access token is required, see `x-mapbox --help`.

Options:
  --profile [mapbox.driving|mapbox.walking|mapbox.cycling]
                                  Mapbox direction profile id
  --alternatives / --no-alternatives
                                  Generate alternative routes?
  --instructions [text|html]      Format for route instructions
  --geometry [geojson|polyline|false]
                                  Geometry encoding
  --steps / --no-steps            Include steps in the response
  --geojson / --no-geojson        Return geojson feature collection (default:
                                  full response json)
  -o, --output TEXT               Save output to a file.
  --help                          Show this message and exit.
```

### distance
```
Usage: x-mapbox distance [OPTIONS] [WAYPOINTS]...

  The Distance API returns all travel times between many points (also known
  as Distance Matrix). This is often used as input for solving routing
  optimization problems.

    $ x-mapbox distance "[-122.681, 45.528]" "[-122.716, 45.525]"

  The output is a json object with a "durations" key containing a 2D array
  of travel times between waypoints.

  An access token is required, see `x-mapbox --help`.

Options:
  --profile [driving|walking|cycling]
                                  Mapbox direction profile id
  -o, --output TEXT               Save output to a file.
  --help                          Show this message and exit.
```

### geocoding
```
Usage: x-mapbox geocoding [OPTIONS] [QUERY]

  This command returns places matching an address (forward mode) or places
  matching coordinates (reverse mode).

  In forward (the default) mode the query argument shall be an address such
  as '1600 pennsylvania ave nw'.

    $ x-mapbox geocode '1600 pennsylvania ave nw'

  In reverse mode the query argument shall be a JSON encoded array of
  longitude and latitude (in that order) in decimal degrees.

    $ x-mapbox geocode --reverse '[-77.4371, 37.5227]'

  An access token is required, see `x-mapbox --help`.

Options:
  --forward / --reverse  Perform a forward or reverse geocode. [default:
                         forward]
  -i, --include          Include HTTP headers in the output.
  --lat FLOAT            Bias results toward this latitude (decimal degrees).
                         --lon is also required.
  --lon FLOAT            Bias results toward this longitude (decimal degrees).
                         --lat is also required.
  -t, --place-type NAME  Restrict results to one or more of these place types:
                         ['address', 'country', 'neighborhood', 'place',
                         'poi', 'postcode', 'region'].
  -o, --output TEXT      Save output to a file.
  --help                 Show this message and exit.
```

### staticmap
```
Usage: x-mapbox staticmap [OPTIONS] MAPID OUTPUT

  Generate static map images from existing Mapbox map ids. Optionally
  overlay with geojson features.

    $ x-mapbox staticmap --features features.geojson mapbox.satellite
    out.png   $ x-mapbox staticmap --lon -61.7 --lat 12.1 --zoom 12
    mapbox.satellite out2.png

  An access token is required, see `x-mapbox --help`.

Options:
  --features TEXT              GeoJSON Features to render as overlay
  --lat FLOAT                  Latitude
  --lon FLOAT                  Longitude
  --zoom INTEGER               Zoom
  --size <INTEGER INTEGER>...  Image width and height in pixels
  --help                       Show this message and exit.
```

### surface
```
Usage: x-mapbox surface [OPTIONS] MAPID LAYER FIELDS [WAYPOINTS]...

  Mapbox Surface API enables flexible querying of data stored in vector
  tiles on Mapbox, to create results like elevation profiles.

        $ x-mapbox surface mapbox.mapbox-terrain-v1 contour ele \ 
        "[-122.781, 45.528]" "[-122.716, 45.525]"

  An access token is required, see `x-mapbox --help`.

Options:
  -z, --zoom INTEGER              Zoom level to query (default: 14)
  --interpolate / --no-interpolate
                                  Weighted average interpolation (default:
                                  True)
  --geojson / --no-geojson        Return geojson feature collection (default:
                                  True)
  -o, --output TEXT               Save output to a file.
  --help                          Show this message and exit.
```

### upload
```
Usage: x-mapbox upload [OPTIONS] TILESET INFILE

  Upload data to Mapbox accounts. All endpoints require authentication.
  Uploaded data lands at https://www.mapbox.com/data/ and can be used in new
  or existing projects.

    $ x-mapbox upload username.data data.geojson

  Note that the tileset must start with your username. An access token with
  upload scope is required, see `x-mapbox --help`.

Options:
  --name TEXT  Name for the data upload
  --help       Show this message and exit.
```
