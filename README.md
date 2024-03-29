# Interline Routetester


<!-- the following is generated by: npx markdown-toc -i README.md -->

<!-- toc -->

- [Features](#features)
- [Installation](#installation)
- [Acceptance Testing](#acceptance-testing)
  * [Input Format and Parameters](#input-format-and-parameters)
    + [Metadata](#metadata)
    + [Request Inputs](#request-inputs)
    + [Response Matchers](#response-matchers)
    + [Route Request Modes](#route-request-modes)
  * [Automatically Generate Input Files from Origin/Destination Points](#automatically-generate-input-files-from-origindestination-points)
  * [Command-line Usage](#command-line-usage)
  * [Output Format](#output-format)
- [Load Testing](#load-testing)
- [Comparison Testing](#comparison-testing)
- [Routing Engines Requiring API Keys](#routing-engines-requiring-api-keys)

<!-- tocstop -->

## Features

Interline uses the Routetester to "battle harden" and run quality assurance on our routing engines. That is, this package can be used to perform load testing, acceptance testing, and comparison testing.

Routetester includes adapters to run against multiple types of routing engines. Current supported are:

- [OpenTripPlanner](http://www.opentripplanner.org)
- [Valhalla](https://www.interline.io/valhalla/)
- [Google Maps Platform Directions API](https://developers.google.com/maps/documentation/directions/)

## Installation

Make sure you have Python 3.7 available. Then run:

```
python3 ./setup.py install
```

## Acceptance Testing

Run and check particular routing requests. Useful for both automated (using a CI server) and manual quality assurance of routing algorithm, data updates, and costing configuration tuning.

### Input Format and Parameters

Specify tests in one or more GeoJSON files.

Each GeoJSON file should contain a `FeatureCollection` where each feature is a GeoJSON `LineString` geometry. The first point on the line will be used as the journey origin. The final point on the line will be used as the journey destination. Each feature should have a `properties` object that refines the route request and specifies matchers to use to accept (or reject) the route response.

To create and edit the input GeoJSON files, try an editor like [geojson.io](http://geojson.io)

#### Metadata

property name | format
------------- | ------
title | string

Follows [mapbox/simplestyle-spec](https://github.com/mapbox/simplestyle-spec)

#### Request Inputs

- origin is first point in `LineString` geometry
- destination is last point in `LineString` geometry
- intermediate points are ignored for now

property name | format
---- | ------
mode | enum, see [route request modes](#route-request-modes)
when | natural language date, e.g. "next tuesday at 9am"; parsed using [parsedatetime](https://github.com/bear/parsedatetime)
timing | enum: [`departBy` (default), `arriveBy`]
extraRequestParams | object

Open questions:
- how to handle transit vehicle preference? (OTP and Valhalla handle this differently)

Adapters
- OpenTripPlanner `plan` endpoint: http://dev.opentripplanner.org/apidoc/1.4.0/resource_PlannerResource.html
- Valhalla `route` endpoint: https://valhalla.readthedocs.io/en/latest/api/turn-by-turn/api-reference/
- Google Directions API: https://developers.google.com/maps/documentation/directions/intro#DirectionsRequests

#### Response Matchers

name | format
---- | ------
httpStatusCode | integer
minDuration | seconds
maxDuration | seconds
minOverallDistance | meters
maxOverallDistance | meters
minWalkingDistance | meters
maxWalkingDistance | meters
minTransitLegs | integer
maxTransitLegs | integer
includesRoute | string
excludesRoute | string
includesTrip | string
excludesTrip | string
includesStop | string
excludeStop | string
includesAgency | string
excludesAgency | string

Adapters
- OpenTripPlanner JSON response: http://dev.opentripplanner.org/apidoc/1.3.0/json_Response.html
- Valhalla JSON response: https://github.com/valhalla/valhalla/blob/master/docs/api/turn-by-turn/api-reference.md#outputs-of-a-route
- Google Directions JSON response: https://developers.google.com/maps/documentation/directions/intro#DirectionsResponses

#### Route Request Modes

mode | OpenTripPlanner request | Valhalla request
--------- | ----------- | ----------------
`walk+transit` | `transit,walk` | `multimodal`
... | ... | ...

### Automatically Generate Input Files from Origin/Destination Points

This package includes a simple tool, `routetester.starbucks`, to automatically generate tests. By default it uses a global database of Starbucks locations (thus, the name).

It can also sample from any GeoJSON file containing `Point` features. You can prepare a GeoJSON file with points of interest/landmarks around a region, and run this command to generate a full GeoJSON file for request/response testing of each possible journey.

Usage:

```sh
usage: routetester.starbucks [-h] [--infile INFILE] [--origins ORIGINS]
                             [--destinations DESTINATIONS]
                             [--mindistance MINDISTANCE]
                             [--maxdistance MAXDISTANCE] [--bbox BBOX]
                             outfile

Generate OD features from Starbucks locations or a GeoJSON file of points of
interest

positional arguments:
  outfile               Output GeoJSON

optional arguments:
  -h, --help            show this help message and exit
  --infile INFILE       Input GeoJSON
  --origins ORIGINS     Number of origins
  --destinations DESTINATIONS
                        Number of destinations for each origin
  --mindistance MINDISTANCE
                        Minimum distance between origins/destinations (in
                        kilometers)
  --maxdistance MAXDISTANCE
                        Minimum distance between origins/destinations (in
                        kilometers)
  --bbox BBOX           bbox
```

Here is an example of creating test journeys between Starbucks locations in London, and extracting the titles of all the tests using [jq](https://stedolan.github.io/jq/):

```sh
# routetester.starbucks --bbox=-1.197510,51.151786,0.736084,51.903613 --origins=3 --destinations=2 starbucks-london.geojson

# jq '.features[].properties.title' starbucks-london.geojson  | sort
"Baker Street/Porter Street -> SSP Liverpool St Kiosk"
"Baker Street/Porter Street -> Victoria Street & Horwick Place"
"Hampton - Sainsbury's -> Ealing - The Green"
"Hampton - Sainsbury's -> Kew - Station Parade"
"New Oxford Street -> DSGI Fulham"
"New Oxford Street -> Minories"
```

### Command-line Usage

Here is how to use the main `routetester` command:


```sh
usage: routetester [-h] [--mode MODE] [--when WHEN] [-v] [--debug] [-o OUT]
                   [-c COUNT]
                   url testfiles [testfiles ...]

Route Tester

positional arguments:
  url                   Test endpoint
  testfiles             Test GeoJSON input file

optional arguments:
  -h, --help            show this help message and exit
  --mode MODE           Planner: otp or valhalla
  --when WHEN           Override all trip date/times, e.g. "next monday at
                        10am"
  -v, --verbose         Print urls and failures
  --debug               Print debug information
  -o OUT, --out OUT     Save GeoJSON output to file
  -c COUNT, --count COUNT
                        Run each test n times
```

For more information on the `--when` argument, see https://github.com/bear/parsedatetime

Example:

```sh
routetester --mode=otp --when="next monday at 8am" --verbose --count=5 --out=out.geojson http://localhost:8000 starbucks-london.geojson
```

Output, with for the sake of demonstration 2 failed tests:

```
5: Missing route; got 23 expected 8,27
2: Duration out of bounds: got 1509.0, expected max 1500.0, Missing route; got 113 expected X29,N37
```

The exit code will be non-zero if any test produced errors. This is how you can have your CI system fail a build.

### Output Format

The tester can also save the test output as a GeoJSON file for further parsing or visual display. The output is all the test trips in the input files, with a `result` object in each feature's `properties`:

```json
"result": {
  "url": "http://localhost:8000/otp/routers/default/plan?fromPlace=55.97826%2C-3.17381&toPlace=55.89012%2C-3.20129&mode=TRANSIT%2CWALK&maxWalkDistance=800&arriveBy=False&wheelchair=False&date=2018-12-10&time=08%3A00%3A00",
  "ok200": 4,
  "not200": 0,
  "passed": 3,
  "failed": 1,
  "response_time_min": 0.124721,
  "response_time_median": 0.9013355,
  "response_time_max": 1.615394,
  "errors": "Duration out of bounds: got 8128, expected max 5400.0",
  "responses": [ "... responses and itinerary summaries ..." ]
}
```

Paste this output into [geojson.io](http://geojson.io) or [geojson.tools](http://geojson.tools/) and you will see successfull tests drawn as <span style="color: green;">green lines</span> and failed tests as <span style="color: red;">red lines</span>. Click on a feature to view its properties.

Alternatively, you can parse the output using JSON processing tools. For example, to print just the median response times using [jq](https://stedolan.github.io/jq/):

```sh
# jq '.features[].properties.result.response_time_median' out.geojson
1.158412
0.611312
0.814694
0.709484
1.497549
1.63594
0.773412
```

## Load Testing

The GeoJSON test files can also be used with [Locust](https://locust.io/) to perform load testing using the `routetester.locust` command:

```sh
routetester.locust [--mode MODE] [--testfile TESTFILE] [locust arguments]
```

This shim takes `--mode` (otp, valhalla) and `--testfile` (GeoJSON input file) options, and passes all other arguments to `locust`. To perform a quick 1 minute test with 25 simulated users, for example:

```sh
# routetester.locust --testfile starbucks-london.geojson --host=http://localhost:8000 --no-web -c 25 -r 25 --run-time 1m
[2018-12-03 15:33:07,370] mbp.local/INFO/locust.main: Run time limit set to 60 seconds
[2018-12-03 15:33:07,371] mbp.local/INFO/locust.main: Starting Locust 0.9.0
[2018-12-03 15:33:07,371] mbp.local/INFO/locust.runners: Hatching and swarming 25 clients at the rate 25 clients/s...
... snip ...
Percentage of the requests completed within given times
 Name                                # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%
-----------------------------------------------------------------------------------------------------------
 GET /otp/routers/default/plan?...       49   1000   1100   1100   1100   1200   1600   2200   2200   2200
 GET /otp/routers/default/plan?...       46   1600   1700   1700   1800   1900   2100   2600   2600   2600
 GET /otp/routers/default/plan?...       52   1400   1400   1500   1500   1700   2100   2200   2300   2300
 GET /otp/routers/default/plan?...       55   1900   1900   2100   2100   2300   2700   2800   2900   2900
 GET /otp/routers/default/plan?...       63    670    700    760    780   1000   1100   1800   2200   2200
 GET /otp/routers/default/plan?...       49    940   1000   1100   1200   1300   1300   2600   2600   2600
 GET /otp/routers/default/plan?...       48    500    550    590    620    740    770   1100   1100   1100
-----------------------------------------------------------------------------------------------------------
 Total                                  362   1100   1400   1600   1700   1900   2100   2300   2600   2900
```

You can also start the Locust web server and view results and charts interactively:

```sh
# routetester.locust --testfile starbucks-london.geojson --host=http://localhost:8000
[2018-12-03 15:35:15,309] mbp.local/INFO/locust.main: Starting web monitor at *:8089
[2018-12-03 15:35:15,309] mbp.local/INFO/locust.main: Starting Locust 0.9.0
```

and view the results on http://localhost:8089. See the [Locust documentation](https://docs.locust.io/en/stable/) for more options.

## Comparison Testing

When validating whether a new routing engine returns quality results, it can be useful to compare results from multiple routine engines.

The `routertester.compare` tool take the [same input data format](#input-formats-and-parameters) as the `routetester` command.

Usage:

```sh
usage: routetester.compare [-h] [--when WHEN] [--whentz WHENTZ] [-v] [--debug]
                           testfile outfile modes [modes ...]

Make requests to multiple routing engines and compare the results

positional arguments:
  testfile         Test GeoJSON input file
  outfile          GeoJSON output file
  modes

optional arguments:
  -h, --help       show this help message and exit
  --when WHEN      Override all trip date/times, e.g. "next monday at 10am"
  --whentz WHENTZ  Timezone for --when
  -v, --verbose    Print urls and failures
  --debug
```

Here is an example invocation:

```sh
routetester.compare starbucks-london.geojson compare.geojson otp http://localhost:8000 google https://maps.googleapis.com --verbose
```

Output is provided in GeoJSON format.

## Routing Engines Requiring API Keys

Some routing engines require an API key. Specify your API key using the following environment variables:

- `GOOGLE_MAPS_API_KEY` for Google Directions API
- `VALHALLA_API_KEY` for Interline Valhalla
