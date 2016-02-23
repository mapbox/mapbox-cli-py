# Geocoding

Let's geocode some addresses. Here we use [`jq`](https://stedolan.github.io/jq/) to parse the first (most relevant) feature from the returned GeoJSON feature collection.
```
$ mapbox geocoding "4001 Southwest Canyon Road, Portland, OR" | jq -c .features[0] >> waypoints.txt
$ mapbox geocoding "1945 SE Water Ave, Portland, OR" | jq -c .features[0] >> waypoints.txt
```

generate static maps,
```
$ cat waypoints.txt | mapbox staticmap --features - mapbox.streets out.png
```
![pdx](https://gist.githubusercontent.com/perrygeo/eef0db7967d0db1b05d4/raw/82214f6592db39cfbba6f8a161e894cddb6087d9/out.png)

Or batch geocode text files
```
$ mapbox geocoding places.txt | jq -c .features[0] | fio collect > places.geojson
```
