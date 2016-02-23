# Surface

Find the elevations of the waypoints using the surface API

```
$ mapbox surface mapbox.mapbox-terrain-v1 contour ele < waypoints.txt \
    | jq .features[0].properties.ele
210
```
