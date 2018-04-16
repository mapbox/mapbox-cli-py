# Analytics

__Accounts__:

A Mapbox user wants information on API usage over a specific period of time.  The user's username is "mapbox-user", and the period of interest is 2018 April 15-16.

```
$ mapbox analytics \
  --resource-type accounts \
  --username mapbox-user \
  --start 2018-04-15T00:00:00.000Z \
  --end 2018-04-16T00:00:00.000Z

{
  "period": [ "2018-04-15T00:00:00.000Z", "2018-04-16T00:00:00.000Z" ],
  "timestamps": [ "2018-04-15T00:00:00.000Z", "2018-04-16T00:00:00.000Z" ],
  "services": {
    "mapview": [ 0, 5 ],
    "static": [ 10, 15 ],
    "tiles": [ 20, 25 ],
    "directions": [ 30, 35 ],
    "geocode": [ 40, 45 ]
  }
}
```

__Tokens__:

A Mapbox user wants information on API usage associated with a specific token over a specific period of time.  The user's username is "mapbox-user", the token id is "mapbox-token", and the period of interest is 2018 April 15-16.

```
$ mapbox analytics \
  --resource-type tokens \
  --username mapbox-user \
  --id mapbox-token \
  --start 2018-04-15T00:00:00.000Z \
  --end 2018-04-16T00:00:00.000Z

{
  "period": [ "2018-04-15T00:00:00.000Z", "2018-04-16T00:00:00.000Z" ],
  "timestamps": [ "2018-04-15T00:00:00.000Z", "2018-04-16T00:00:00.000Z" ],
  "services": {
    "mapview": [ 0, 5 ],
    "static": [ 10, 15 ],
    "tiles": [ 20, 25 ],
    "directions": [ 30, 35 ],
    "geocode": [ 40, 45 ]
  }
}
```

__Styles__:

A Mapbox user wants information on API usage associated with a specific style over a specific period of time.  The user's username is "mapbox-user", the style id is "mapbox-style", and the period of interest is 2018 April 15-16.

```
$ mapbox analytics \
  --resource-type styles \
  --username mapbox-user \
  --id mapbox-style \
  --start 2018-04-15T00:00:00.000Z \
  --end 2018-04-16T00:00:00.000Z

{
  "period": [ "2018-04-15T00:00:00.000Z", "2018-04-16T00:00:00.000Z" ],
  "timestamps": [ "2018-04-15T00:00:00.000Z", "2018-04-16T00:00:00.000Z" ],
  "services": {
    "mapview": [ 0, 5 ],
    "static": [ 10, 15 ],
    "tiles": [ 20, 25 ]
  }
}
```

__Tilesets__:

A Mapbox user wants information on API usage associated with a specific tileset over a specific period of time.  The user's username is "mapbox-user", the map id is "mapbox.streets", and the period of interest is 2018 April 15-16.

```
$ mapbox analytics \
  --resource-type tilesets \
  --username mapbox-user \
  --id mapbox.streets \
  --start 2018-04-15T00:00:00.000Z \
  --end 2018-04-16T00:00:00.000Z

{
  "period": [ "2018-04-15T00:00:00.000Z", "2018-04-16T00:00:00.000Z" ],
  "timestamps": [ "2018-04-15T00:00:00.000Z", "2018-04-16T00:00:00.000Z" ],
  "services": {
    "mapview": [ 0, 5 ],
    "static": [ 10, 15 ],
    "tiles": [ 20, 25 ]
  }
}
```
