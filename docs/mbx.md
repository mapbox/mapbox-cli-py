# mbx

`mbx` is a command line interface to Mapbox web services. 

## Access Token

Mapbox web services require an access token. Your token is shown on the
https://www.mapbox.com/developers/api/ page when you are logged in. The
token can be provided on the command line

    $ mbx --access-token MY_TOKEN ...

or as an environment variable named MAPBOX_ACCESS_TOKEN or
MapboxAccessToken.

    $ export MAPBOX_ACCESS_TOKEN=MY_TOKEN
    $ mbx ...

## Usage

```
$ mbx --help
Usage: mbx [OPTIONS] COMMAND [ARGS]...

    This is the command line interface to Mapbox web services.

    Mapbox web services require an access token. Your token is shown on the
    https://www.mapbox.com/developers/api/ page when you are logged in. The
    token can be provided on the command line

    $ mbx --access-token MY_TOKEN ...

    or as an environment variable named MAPBOX_ACCESS_TOKEN or
    MapboxAccessToken.

    $ export MAPBOX_ACCESS_TOKEN=MY_TOKEN
    $ mbx ...

Options:
    --access-token TEXT  Your Mapbox access token.
    -v, --verbose        Increase verbosity.
    --version            Show the version and exit.
    -q, --quiet          Decrease verbosity.
    --help               Show this message and exit.

Commands:
    geocode  Geocode an address or coordinates.
```
