# Distances

The distances command allows us to build a "distance matrix" of travel times between up to 25 cities.
Remember those big tables in the back of your road atlas? Yeah those.

Let's say we have a list of the top 10 US cities by population

```
New York, NY
Los Angeles, CA
Chicago, IL
Houston, TX
Philadelphia, PA
Phoenix, AZ
San Antonio, TX
San Diego, CA
Dallas, TX
San Jose, CA
```

We can geocode them and collect the first result into a GeoJSON FeatureCollection

```
mapbox geocoding cities.txt | jq -c .features[0] | fio collect > cities.geojson
```

And get the distance matrix

```json
$ mapbox distance cities.geojson
{"code":"Ok","durations":[[0,167831,49679,99841,6385,151367,110869,172138,96671,126259],[167582,0,120007,97296,162470,21459,86329,7640,88247,61862],[49656,120266,0,72749,46625,110777,76741,124788,59696,86483],[99708,96925,72573,0,94939,75648,11282,92350,16394,42527],[6453,162922,46719,95026,0,146458,106054,167229,91856,121350],[150979,21491,110549,76109,145867,0,65143,21124,70332,40675],[110752,85976,76471,11281,105984,64699,0,81402,17184,31579],[171764,7672,124193,92794,166652,21126,81827,0,87920,57360],[96656,87683,59523,16330,91888,69773,17195,87486,0,34362],[126087,61525,86162,42593,120975,40248,31626,56950,34392,0]]}
```

A bit hard to interpret visually but the data is all there. To get the travel time (in seconds) between 
Chicago (at index 2) and Phoenix (index 5):

```
$ mapbox distance cities.geojson | jq ".durations[2][5]"
110777
```
