# Tilequery

Access the Mapbox Tilequery API from the command line.

# Querying a Tileset

To query a tileset for specific features, run `mapbox tilequery`, passing in values for `map_id`, `lon`, and `lat`.

```
mapbox tilequery mapbox.mapbox-streets-v10 0.0 1.1
```

Use the `--radius`, `--limit`, `--dedupe`, `--geometry`, `--layer`, and `--output` options for additional functionality.

# Notes

To query multiple tilesets, pass in multiple values for `map_id`.

```
mapbox tilequery mapbox.mapbox-streets-v10 mapbox.mapbox-outdoors-v10 0.0 1.1
```

To query a negative longitudinal or latitudinal value, precede it with `--`.

__longitude__:

```
mapbox tilequery mapbox.mapbox-streets-v10 -- -0.0 1.1
```

__latitude__:

```
mapbox tilequery mapbox.mapbox-streets-v10 0.0 -- -1.1
```

To query multiple layers, use the `--layer` option more than once.

```
mapbox tilequery --layer layer0 --layer layer1 mapbox.mapbox-streets-v10 0.0 1.1
```

# Viewing Help

For help, use the `--help` option.

```
mapbox tilequery --help
```
