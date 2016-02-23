# Turn by Turn Directions



Here we use [`jq`](https://stedolan.github.io/jq/) to parse json results and [geojsonio](https://github.com/mapbox/geojson.io) for quick map creation.

First, we take two addresses between which we'll find directions. We geocode them and parse the first (most relevant) feature from the returned GeoJSON feature collection.

```
$ mapbox geocoding "4001 Southwest Canyon Road, Portland, OR" | jq -c .features[0] > waypoints.txt
$ mapbox geocoding "1945 SE Water Ave, Portland, OR" | jq -c .features[0] >> waypoints.txt
```

Now find travel directions between them as a geojson Feature collection, then piping the result to geojsonio
```
$ mapbox directions --geojson < waypoints.txt | geojsonio
```

Which opens a web browser to [an interactive web map](http://bl.ocks.org/d/07c9145cfe465467f7e2).

If you're more interested in the turn-by-turn directions than the map, you can parse the full directions response

```
$ mapbox directions < waypoints.txt | jq '.routes[0].steps[]  .maneuver.instruction'

"Head northeast on Southwest Zoo Road"
"Make a sharp left"
"Bear left"
"Continue"
"Turn left onto Southwest Knights Boulevard"
"Turn left"
"Continue on Sunset Highway (US 26)"
"Continue on Vista Ridge Tunnel (US 26)"
"Continue on Sunset Highway (US 26)"
"Continue on US 26"
"Continue on Stadium Freeway (I 405;US 26)"
"Continue on Stadium Freeway (I 405)"
"Continue"
"Continue on Marquam Bridge (I 5)"
"Continue on Eastbank Freeway (I 5)"
"Continue"
"Continue"
"Turn right onto Southeast Water Avenue"
"Turn right"
"Continue"
"Continue"
"You have arrived at your destination"
```
