# mapbox-cli-py

[![Build Status](https://travis-ci.org/mapbox/mapbox-cli-py.svg?branch=master)](https://travis-ci.org/mapbox/mapbox-cli-py) [![Coverage Status](https://coveralls.io/repos/mapbox/mapbox-cli-py/badge.svg?branch=master&service=github)](https://coveralls.io/github/mapbox/mapbox-cli-py?branch=master)

Command line interface to Mapbox Web Services based on https://github.com/mapbox/mapbox-sdk-py.

## Installation

**For users on OS X**, we recommend installing with [homebrew](http://brew.sh/)
```
$ brew install mapbox/cli/mapbox
```

**For users familiar with Python** and who already have [`pip`](https://pip.pypa.io/en/stable/installing/) installed on their system, you can create a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) and install with
```
(venv)$ pip install mapboxcli
```

Installing locally without a virtual environment using
```
$ pip install --user mapboxcli
```
You'll then need to include `~/.local/bin` in your $PATH.

Installing globally is *not recommended* but some users may want to do so under certain circumstances
```
$ sudo pip install mapboxcli
```

If you're interested in contributing, you'll want to [install from master branch](https://github.com/mapbox/mapbox-cli-py/blob/master/CONTRIBUTING.md#contributing).

## Setup

Use of the `mapbox` command line interface requires an access token.
Your token is shown on the [API access tokens](https://www.mapbox.com/studio/account/tokens/) page when you are logged in.
The token can be provided on the command line

```
$ mapbox --access-token MY_TOKEN ...
```

or as an environment variable named `MAPBOX_ACCESS_TOKEN`

```
$ export MAPBOX_ACCESS_TOKEN=MY_TOKEN
$ mapbox ...
```

## Usage

* [directions](#directions)
* [geocoding](#geocoding)
* [mapmatching](#mapmatching)
* [staticmap](#staticmap)
* [upload](#upload)
* [datasets](#datasets)

For any command that takes waypoints or features as an input you can either specify:

* Coordinate pair(s) of the form `"[0, 0]"` or `"0,0"` or `"0 0"`
* Sequence of GeoJSON features on `stdin`
* GeoJSON FeatureCollection on `stdin`
* Paths to GeoJSON file(s) containing either a single Feature or FeatureCollection.

Note that functions that accept points only, any non-point feature is filtered out.

### directions
```
Usage: mapbox directions [OPTIONS] FEATURES...

  The Mapbox Directions API will show you how to get where you're going.

  mapbox directions "[0, 0]" "[1, 1]"

  An access token is required.  See "mapbox --help".

Options:
  --profile [mapbox/driving|mapbox/driving-traffic|mapbox/walking|mapbox/cycling]
                                  Routing profile
  --alternatives / --no-alternatives
                                  Whether to try to return alternative routes
  --geometries [geojson|polyline|polyline6]
                                  Format of returned geometry
  --overview [full|simplified|False]
                                  Type of returned overview geometry
  --steps / --no-steps            Whether to return steps and turn-by-turn
                                  instructions
  --continue-straight / --no-continue-straight
                                  Whether to see the allowed direction of
                                  travel when departing the original waypoint
  --waypoint-snapping TEXT        Controls waypoint snapping
  --annotations TEXT              Additional metadata along the route
  --language TEXT                 Language of returned turn-by-turn
                                  instructions
  -o, --output TEXT               Save output to a file
  --help                          Show this message and exit.
```


### geocoding
```
Usage: mapbox geocoding [OPTIONS] [QUERY]

  This command returns places matching an address (forward mode) or places
  matching coordinates (reverse mode).

  In forward (the default) mode the query argument shall be an address such
  as '1600 pennsylvania ave nw'.

    $ mapbox geocoding '1600 pennsylvania ave nw'

  In reverse mode the query argument shall be a JSON encoded array of
  longitude and latitude (in that order) in decimal degrees.

    $ mapbox geocoding --reverse '[-77.4371, 37.5227]'

  An access token is required, see `mapbox --help`.

Options:
  --forward / --reverse           Perform a forward or reverse geocode.
                                  [default: forward]
  -i, --include                   Include HTTP headers in the output.
  --lat FLOAT                     Bias results toward this latitude (decimal
                                  degrees). --lon is also required.
  --lon FLOAT                     Bias results toward this longitude (decimal
                                  degrees). --lat is also required.
  -t, --place-type NAME           Restrict results to one or more place types.
  -o, --output TEXT               Save output to a file.
  -d, --dataset [mapbox.places|mapbox.places-permanent]
                                  Source dataset for geocoding, [default:
                                  mapbox.places]
  --country TEXT                  Restrict forward geocoding to specified
                                  country codes,comma-separated
  --bbox TEXT                     Restrict forward geocoding to specified
                                  bounding box,given in minX,minY,maxX,maxY
                                  coordinates.
  --features                      Return results as line-delimited GeoJSON
                                  Feature sequence, not a FeatureCollection
  --limit INTEGER                 Limit the number of returned features
  --help                          Show this message and exit.
```

### mapmatching
```
Usage: mapbox mapmatching [OPTIONS] FEATURES...

  Mapbox Map Matching API lets you use snap your GPS traces to the
  OpenStreetMap road and path network.

        $ mapbox mapmatching trace.geojson

  An access token is required, see `mapbox --help`.

Options:
  --gps-precision INTEGER         Assumed precision of tracking device
                                  (default 4 meters)
  --profile [mapbox.driving|mapbox.cycling|mapbox.walking]
                                  Mapbox profile id
  --help                          Show this message and exit.
```

### staticmap
```
Usage: mapbox staticmap [OPTIONS] MAPID OUTPUT

  Generate static map images from existing Mapbox map ids. Optionally
  overlay with geojson features.

    $ mapbox staticmap --features features.geojson mapbox.satellite out.png
    $ mapbox staticmap --lon -61.7 --lat 12.1 --zoom 12 mapbox.satellite
    out2.png

  An access token is required, see `mapbox --help`.

Options:
  --features TEXT              GeoJSON Features to render as overlay
  --lat FLOAT                  Latitude
  --lon FLOAT                  Longitude
  --zoom INTEGER               Zoom
  --size <INTEGER INTEGER>...  Image width and height in pixels
  --help                       Show this message and exit.
```


### upload
```
Usage: mapbox upload [OPTIONS] TILESET [INFILE]

  Upload data to Mapbox accounts. All endpoints require authentication.
  Uploaded data lands at https://www.mapbox.com/studio/tilesets/ and can be used in new
  or existing projects.

  You can specify the tileset id and input file

    $ mapbox upload username.data mydata.geojson

  Or specify just the tileset id and take an input file on stdin

    $ cat mydata.geojson | mapbox upload username.data

  The --name option defines the title as it appears in Studio and defaults
  to the last part of the tileset id, e.g. "data"

  Note that the tileset must start with your username. An access token with
  upload scope is required, see `mapbox --help`.

Options:
  --name TEXT  Name for the data upload
  --help       Show this message and exit.
```

### datasets
```
Usage: mapbox datasets [OPTIONS] COMMAND [ARGS]...

  Read and write GeoJSON from Mapbox-hosted datasets

  All endpoints require authentication. An access token with appropriate
  dataset scopes is required, see `mapbox --help`.

  Note that this API is currently a limited-access beta.

Options:
  --help  Show this message and exit.

Commands:
  create                 Create an empty dataset
  create-tileset         Generate a tileset from a dataset
  delete-dataset         Delete a dataset
  delete-feature         Delete a single feature from a dataset
  list                   List datasets
  list-features          List features in a dataset
  put-feature            Insert or update a single feature in a dataset
  read-dataset           Return information about a dataset
  read-feature           Read a single feature from a dataset
  update-dataset         Update information about a dataset
```

### datasets list
```
Usage: mapbox datasets list [OPTIONS]

  List datasets.

  Prints a list of objects describing datasets.

      $ mapbox datasets list

  All endpoints require authentication. An access token with `datasets:read`
  scope is required, see `mapbox --help`.

Options:
  -o, --output TEXT  Save output to a file
  --help             Show this message and exit.
```

### datasets create
```
Usage: mapbox datasets create [OPTIONS]

  Create a new dataset.

  Prints a JSON object containing the attributes of the new dataset.

      $ mapbox datasets create

  All endpoints require authentication. An access token with
  `datasets:write` scope is required, see `mapbox --help`.

Options:
  -n, --name TEXT         Name for the dataset
  -d, --description TEXT  Description for the dataset
  --help                  Show this message and exit.
```

### datasets read-dataset
```
Usage: mapbox datasets read-dataset [OPTIONS] DATASET

  Read the attributes of a dataset.

  Prints a JSON object containing the attributes of a dataset. The
  attributes: owner (a Mapbox account), id (dataset id), created (Unix
  timestamp), modified (timestamp), name (string), and description (string).

      $ mapbox datasets read-dataset dataset-id

  All endpoints require authentication. An access token with `datasets:read`
  scope is required, see `mapbox --help`.

Options:
  -o, --output TEXT  Save output to a file
  --help             Show this message and exit.
```

### datasets update-dataset
```
Usage: mapbox datasets update-dataset [OPTIONS] DATASET

  Update the name and description of a dataset.

  Prints a JSON object containing the updated dataset attributes.

      $ mapbox datasets update-dataset dataset-id

  All endpoints require authentication. An access token with
  `datasets:write` scope is required, see `mapbox --help`.

Options:
  -n, --name TEXT         Name for the dataset
  -d, --description TEXT  Description for the dataset
  --help                  Show this message and exit.
```

### datasets delete-dataset
```
Usage: mapbox datasets delete-dataset [OPTIONS] DATASET

  Delete a dataset.

      $ mapbox datasets delete-dataset dataset-id

  All endpoints require authentication. An access token with
  `datasets:write` scope is required, see `mapbox --help`.

Options:
  --help  Show this message and exit.
```

### datasets list-features
```
Usage: mapbox datasets list-features [OPTIONS] DATASET

  Get features of a dataset.

  Prints the features of the dataset as a GeoJSON feature collection.

      $ mapbox datasets list-features dataset-id

  All endpoints require authentication. An access token with `datasets:read`
  scope is required, see `mapbox --help`.

Options:
  -r, --reverse TEXT  Read features in reverse
  -s, --start TEXT    Feature id to begin reading from
  -l, --limit TEXT    Maximum number of features to return
  -o, --output TEXT   Save output to a file
  --help              Show this message and exit.
```

### datasets put-feature
```
Usage: mapbox datasets put-feature [OPTIONS] DATASET FID [FEATURE]

  Create or update a dataset feature.

  The semantics of HTTP PUT apply: if the dataset has no feature with the
  given `fid` a new feature will be created. Returns a GeoJSON
  representation of the new or updated feature.

      $ mapbox datasets put-feature dataset-id feature-id 'geojson-feature'

  All endpoints require authentication. An access token with
  `datasets:write` scope is required, see `mapbox --help`.

Options:
  -i, --input TEXT  File containing a feature to put
  --help            Show this message and exit.
```

### datasets read-feature
```
Usage: mapbox datasets read-feature [OPTIONS] DATASET FID

  Read a dataset feature.

  Prints a GeoJSON representation of the feature.

      $ mapbox datasets read-feature dataset-id feature-id

  All endpoints require authentication. An access token with `datasets:read`
  scope is required, see `mapbox --help`.

Options:
  -o, --output TEXT  Save output to a file
  --help             Show this message and exit.
```

### datasets delete-feature
```
Usage: mapbox datasets delete-feature [OPTIONS] DATASET FID

  Delete a feature.

      $ mapbox datasets delete-feature dataset-id feature-id

  All endpoints require authentication. An access token with
  `datasets:write` scope is required, see `mapbox --help`.

Options:
  --help  Show this message and exit.
```

### datasets create-tileset
```
Usage: mapbox datasets create-tileset [OPTIONS] DATASET TILESET

  Create a vector tileset from a dataset.

      $ mapbox datasets create-tileset dataset-id username.data

  Note that the tileset must start with your username and the dataset must
  be one that you own. To view processing status, visit
  https://www.mapbox.com/data/. You may not generate another tilesets from
  the same dataset until the first processing job has completed.

  All endpoints require authentication. An access token with `uploads:write`
  scope is required, see `mapbox --help`.

Options:
  -n, --name TEXT  Name for the tileset
  --help           Show this message and exit.
```

## Alternative command syntax

When saving a fraction of a second matters you can call the mapboxcli module
directly instead of using the installed program.

```$ python -m mapboxcli --help```
