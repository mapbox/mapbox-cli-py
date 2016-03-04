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
* [distance](#distance)
* [geocoding](#geocoding)
* [mapmatching](#mapmatching)
* [staticmap](#staticmap)
* [surface](#surface)
* [upload](#upload)
* [datasets](#datasets) (Note: this API is currently in private beta. Any requests to this API from outside of Mapbox will result in a 404.)

For any command that takes waypoints or features as an input you can either specify:

* Coordinate pair(s) of the form `"[0, 0]"` or `"0,0"` or `"0 0"`
* Sequence of GeoJSON features on `stdin`
* GeoJSON FeatureCollection on `stdin`
* Paths to GeoJSON file(s) containing either a single Feature or FeatureCollection.

Note that functions that accept points only, any non-point feature is filtered out.

### directions
```
Usage: mapbox directions [OPTIONS] FEATURES...

  Calculate optimal route with turn-by-turn directions between up to 25
  waypoints.

    $ mapbox directions "[-122.681032, 45.528334]" "[-122.71679, 45.525135]"

  An access token is required, see `mapbox --help`.

Options:
  --profile [mapbox.driving|mapbox.cycling|mapbox.walking]
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
Usage: mapbox distance [OPTIONS] FEATURES...

  The Distance API returns all travel times between many points (also known
  as Distance Matrix). This is often used as input for solving routing
  optimization problems.

    $ mapbox distance "[-122.681, 45.528]" "[-122.716, 45.525]"

  The output is a json object with a "durations" key containing a 2D array
  of travel times between waypoints.

  An access token is required, see `mapbox --help`.

Options:
  --profile [driving|cycling|walking]
                                  Mapbox direction profile id
  -o, --output TEXT               Save output to a file.
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
  --bbox TEXT                     Restrict forward geocoding to specified
                                  bounding box,given in minX,minY,maxX,maxY
                                  coordinates.
  --country TEXT                  Restrict forward geocoding to specified
                                  country codes,comma-separated
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

### surface
```
Usage: mapbox surface [OPTIONS] MAPID LAYER FIELDS FEATURES...

  Mapbox Surface API enables flexible querying of data stored in vector
  tiles on Mapbox, to create results like elevation profiles.

        $ mapbox surface mapbox.mapbox-terrain-v1 contour ele \ 
        "[-122.781, 45.528]" "[-122.716, 45.525]"

  An access token is required, see `mapbox --help`.

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
Usage: mapbox upload [OPTIONS] [INFILE] TILESET

  Upload data to Mapbox accounts. All endpoints require authentication.
  Uploaded data lands at https://www.mapbox.com/data/ and can be used in new
  or existing projects.

  You can specify the input file and tileset id

    $ mapbox upload mydata.geojson username.data

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
  append          Move data from one dataset or file to another, appending to
                  the destination
  read            Print the contents of a dataset to stdout
  create-tileset  Generate a tileset from a dataset
  list            List datasets or features in a dataset
  put             Move data from one dataset or file to another, overwriting
                  the destination
```

### datasets append
```
Usage: mapbox datasets append [OPTIONS] SOURCE DESTINATION

  Move data from one dataset or file to another, appending to the
  destination file or dataset.

  Note that in order to append to a file, the file must be a sequence of
  GeoJSON features and not a FeatureCollection. You must specify --sequence
  in this case.

  Data to copy is indicated by either a dataset URI, a file path, or - to
  represent stdin/stdout. Below are some example operations:

  To append the features from dataset-A to dataset-B:

          $ mapbox datasets append \
          $   mapbox://datasets/username/dataset-A \
          $   mapbox://datasets/username/dataset-B

  To append the features in a local file to dataset-A:

          $ mapbox datasets append \
          $   ~/path/to/my/data.geojson \
          $   mapbox://datasets/username/dataset-A

  To download all the features in dataset-A and append them to a local,
  line-delimited GeoJSON file

          $ mapbox datasets append --sequence \
          $   mapbox://datasets/username/dataset-A \
          $   ~/data.ldgeojson

  All endpoints require authentication. An access token with `uploads:read`
  and/or `uploads:write` scope may be required, see `mapbox --help`.

Options:
  --sequence / --no-sequence  Write a LF-delimited sequence of texts
                              containing individual objects or write a single
                              JSON text containing a feature collection object
                              (the default).
  --rs / --no-rs              Use RS (0x1E) as a prefix for individual texts
                              in a sequence as per http://tools.ietf.org/html
                              /draft-ietf-json-text-sequence-13 (default is
                              False).
  --help                      Show this message and exit.
```

### datasets read
```
Usage: mapbox datasets read [OPTIONS] SOURCE

  Print the contents of a dataset to stdout.

  Data to print is indicated by a dataset URI.

      $ mapbox datasets cat mapbox://datasets/username/dataset-A

  All endpoints require authentication. An access token with `uploads:read`
  scope is required, see `mapbox --help`.

Options:
  --sequence / --no-sequence  Write a LF-delimited sequence of texts
                              containing individual objects or write a single
                              JSON text containing a feature collection object
                              (the default).
  --rs / --no-rs              Use RS (0x1E) as a prefix for individual texts
                              in a sequence as per http://tools.ietf.org/html
                              /draft-ietf-json-text-sequence-13 (default is
                              False).
  --help                      Show this message and exit.
```

### datasets put
```
Usage: mapbox datasets put [OPTIONS] SOURCE DESTINATION

  Move data from one dataset or file to another, overwriting the
  destination.

  Data to copy is indicated by either a dataset URI, a file path, or - to
  represent stdin/stdout. Below are some example operations:

  To replace dataset-B with the contents of dataset-A:

          $ mapbox datasets put \
          $   mapbox://datasets/username/dataset-A \
          $   mapbox://datasets/username/dataset-B

  To replace dataset-A with the contents of a local file:

          $ mapbox datasets put \
          $   ~/path/to/my/data.geojson \
          $   mapbox://datasets/username/dataset-A

  To print the content of a dataset-A to stdout, as line-delimited GeoJSON
  features:

          $ mapbox datasets put --sequence \
          $   mapbox://datasets/username/dataset-A \
          $   -

  To download all the features in dataset-A to a local file, as a GeoJSON
  FeatureCollection:

          $ mapbox datasets put \
          $   mapbox://datasets/username/dataset-A \
          $   ~/data.geojson

  To print feature-1 from dataset-A to stdout:

      $ mapbox datasets put \     $
      mapbox://datasets/username/dataset-A/feature-1 \     $   -

  All endpoints require authentication. An access token with `uploads:read`
  and/or `uploads:write` scope may be required, see `mapbox --help`.

Options:
  --sequence / --no-sequence  Write a LF-delimited sequence of texts
                              containing individual objects or write a single
                              JSON text containing a feature collection object
                              (the default).
  --rs / --no-rs              Use RS (0x1E) as a prefix for individual texts
                              in a sequence as per http://tools.ietf.org/html
                              /draft-ietf-json-text-sequence-13 (default is
                              False).
  --help                      Show this message and exit.
```

### datasets list
```
Usage: mapbox datasets list [OPTIONS] URI

  List datasets or features in a dataset.

      $ mapbox datasets list mapbox://datasets/username     $ mapbox
      datasets list mapbox://datasets/username/dataset-id

  Use this function to list available datasets, printing their URI, name,
  and description. If a URI for a specific dataset is given, the URIs for
  individual features within that dataset are listed.

  All endpoints require authentication. An access token with `uploads:read`
  scope is required, see `mapbox --help`.

Options:
  --help  Show this message and exit.
```

### datasets create-tileset
```
Usage: mapbox datasets create-tileset [OPTIONS] DATASET TILESET

  Create a vector tileset from a dataset.

      $ mapbox datasets create-tileset dataset-id username.data

  Note that the tileset must start with your username and the dataset must
  be one that you own which contains data. To view processing status, visit
  https://www.mapbox.com/data/. You may not generate another tilesets from
  the same dataset until the first processing job has completed.

  All endpoints require authentication. An access token with `uploads:write`
  scope is required, see `mapbox --help`.

Options:
  -n, --name TEXT  Name for the tileset
  --help           Show this message and exit.
```

### datasetsapi
```
Usage: mapbox datasetsapi [OPTIONS] COMMAND [ARGS]...

  Low-level read and write functions for Mapbox datasets

  All endpoints require authentication. An access token with appropriate
  dataset scopes is required, see `mapbox --help`.

  Note that this API is currently a limited-access beta.

Options:
  --help  Show this message and exit.

Commands:
  batch-update-features  Insert, update, or delete multiple features in a
                         dataset
  create-dataset         Create an empty dataset
  delete-dataset         Delete a dataset
  delete-feature         Delete a single feature from a dataset
  list-datasets          List datasets
  list-features          List one page of features from a dataset
  put-feature            Insert or update a single feature in a dataset
  read-dataset           Return information about a dataset
  read-feature           Read a single feature from a dataset
  update-dataset         Update information about a dataset
```

### datasets list-datasets
```
Usage: mapbox datasetsapi list-datasets [OPTIONS]

  List datasets.

  Prints a list of objects describing datasets.

      $ mapbox datasets list-datasets

  All endpoints require authentication. An access token with `datasets:read`
  scope is required, see `mapbox --help`.

Options:
  -o, --output TEXT  Save output to a file
  --help             Show this message and exit.
```

### datasetsapi create-dataset
```
Usage: mapbox datasetsapi create-dataset [OPTIONS]

  Create a new dataset.

  Prints a JSON object containing the attributes of the new dataset.

      $ mapbox datasets create-dataset

  All endpoints require authentication. An access token with
  `datasets:write` scope is required, see `mapbox --help`.

Options:
  -n, --name TEXT         Name for the dataset
  -d, --description TEXT  Description for the dataset
  --help                  Show this message and exit.
```

### datasetsapi read-dataset
```
Usage: mapbox datasetsapi read-dataset [OPTIONS] DATASET

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

### datasetsapi update-dataset
```
Usage: mapbox datasetsapi update-dataset [OPTIONS] DATASET

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

### datasetsapi api delete-dataset
```
Usage: mapbox datasetsapi delete-dataset [OPTIONS] DATASET

  Delete a dataset.

      $ mapbox datasets delete-dataset dataset-id

  All endpoints require authentication. An access token with
  `datasets:write` scope is required, see `mapbox --help`.

Options:
  --help  Show this message and exit.
```

### datasetsapi list-features
```
Usage: mapbox datasetsapi list-features [OPTIONS] DATASET

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

### datasetsapi put-feature
```
Usage: mapbox datasetsapi put-feature [OPTIONS] DATASET FID [FEATURE]

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

### datasetsapi read-feature
```
Usage: mapbox datasetsapi read-feature [OPTIONS] DATASET FID

  Read a dataset feature.

  Prints a GeoJSON representation of the feature.

      $ mapbox datasets read-feature dataset-id feature-id

  All endpoints require authentication. An access token with `datasets:read`
  scope is required, see `mapbox --help`.

Options:
  -o, --output TEXT  Save output to a file
  --help             Show this message and exit.
```

### datasetsapi delete-feature
```
Usage: mapbox datasetsapi delete-feature [OPTIONS] DATASET FID

  Delete a feature.

      $ mapbox datasets delete-feature dataset-id feature-id

  All endpoints require authentication. An access token with
  `datasets:write` scope is required, see `mapbox --help`.

Options:
  --help  Show this message and exit.
```

### datasetsapi batch-update-features
```
Usage: mapbox datasetsapi batch-update-features [OPTIONS] DATASET [PUTS]
                                                [DELETES]

  Update features of a dataset.

  Up to 100 features may be deleted or modified in one request. PUTS should
  be a JSON array of GeoJSON features to insert or updated. DELETES should
  be a JSON array of feature ids to be deleted.

      $ mapbox datasets batch-update-features dataset-id 'puts' 'deletes'

  All endpoints require authentication. An access token with
  `datasets:write` scope is required, see `mapbox --help`.

Options:
  -i, --input TEXT  File containing features to insert, update, and/or delete
  --help            Show this message and exit.
```