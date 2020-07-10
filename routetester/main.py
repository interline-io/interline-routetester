import json
import sys
import argparse
import logging
import requests
import os
import urllib

from .request import Request
from .checker import Checker
from .checkotp import OTPRequest
from .checkvalhalla import ValhallaRequest
from .checkgoogle import GoogleRequest

def main():
    parser = argparse.ArgumentParser(description='Route Tester')
    parser.add_argument('--mode', default='otp', help='Planner: otp or valhalla')
    parser.add_argument('--when', help='Override all trip date/times, e.g. "next monday at 10am"')
    parser.add_argument('--whentz', help='Timezone for --when')
    parser.add_argument('-v', '--verbose', help='Print urls and failures', action='store_true')
    parser.add_argument('--debug', help='Print debug information', action='store_true')
    parser.add_argument('-o', '--out', help='Save GeoJSON output to file')
    parser.add_argument('-c', '--count', help='Run each test n times', default=1, type=int)
    parser.add_argument('-p', '--param', help='Add or override request parameter; example -p costing=auto', action='append')
    parser.add_argument('--map-url', action='store_true', help='Link to open results on geojson.io')
    parser.add_argument('url', help='Test endpoint')
    parser.add_argument('testfiles', nargs='+', help='Test GeoJSON input file')
    args = parser.parse_args()

    # Select planner
    request_cls = Request.get_cls(args.mode)
    if not request_cls:
        print("Unknown planner: %s"%args.mode)
        sys.exit(1)

    # Check params
    params = None
    if args.param:
        params = {}
        for p in args.param:
            key, _, value = p.partition("=")
            params[key] = value

    # Set log level
    level = logging.WARNING
    if args.debug:
        level = logging.DEBUG
    elif args.verbose:
        level = logging.INFO
    logging.basicConfig(format='%(message)s', level=level)

    # Run checker
    checker = Checker(args.url, request_cls, when=args.when, whentz=args.whentz, count=args.count, params=params)
    for filename in args.testfiles:
        checker.load(filename)
    checker.run()

    fc = checker.result_geojson()

    # link to geojson.io
    if args.map_url:
        encodedGeoJson = urllib.parse.quote(json.dumps(fc))
        fc["geojson_io_url"] = f"http://geojson.io/#data=data:application/json,{encodedGeoJson}"
        print(fc["geojson_io_url"])

    # Write geojson output
    if args.out:
        with open(args.out, 'w') as f:
            json.dump(fc, f)

    # Check result
    status = 0
    for trip, rset in checker.rsets.items():
        errors = []
        for r in rset.responses:
            errors += r.errors
        if errors:
            eflat = set([str(i) for i in errors])
            status = 1
            logging.error("%s: %s"%(trip.id, "; ".join(sorted(eflat))))

    sys.exit(status)

if __name__ == "__main__":
    main()