# Maps

Access the Mapbox Maps API from the command line.

# Retrieving Tiles

To retrieve an image tile, vector tile, or UTFGrid, run `mapbox maps tile` with the `--column`, `--row`, and `--zoom-level` options as well as with the `map_id` and `output` arguments.

```
mapbox maps tile --column 0 --row 0 --zoom-level 0 mapbox.streets 0.png
```

Use the `--retina`, `--file-format`, `--style-id`, and `--timestamp` options for additional functionality.

# Retrieving Features

To retrieve vector features from Mapbox Editor projects, run `mapbox maps features` with the `map_id` argument.  To write the output to a file, add the `output` argument.

__writing to the console__:
```
mapbox maps features mapbox.streets
```

__writing to a file__:
```
mapbox maps features mapbox.streets features.json
```

Use the `--feature-format` option for additional functionality.

# Retrieving Metadata

To retrieve TileJSON metadata for a tileset, run `mapbox maps metadata` with the `map_id` argument.  To write the output to a file, add the `output` argument.

__writing to the console__:
```
mapbox maps metadata mapbox.streets
```

__writing to a file__:
```
mapbox maps metadata mapbox.streets metadata.json
```

Use the `--secure` option for additional functionality.

# Retrieving Standalone Markers

To retrieve a single marker image without any background map, run `mapbox maps marker` with the `--marker-name` option and the `output` argument.

```
mapbox maps marker --marker-name pin-s pin-s.png
```

Use the `--label`, `--color`, and `--retina` options for additional functionality.

# Viewing Help

For help, use the `--help` option.

__mapbox maps__:
```
mapbox maps --help
```

__mapbox maps tile__:
```
mapbox maps tile --help
```

__mapbox maps features__:
```
mapbox maps features --help
```

__mapbox maps metadata__:
```
mapbox maps metadata --help
```

__mapbox maps marker__:
```
mapbox maps marker --help
```
