import json
import sys
import argparse
import logging
import csv
import functools

from .request import Request
from .checker import Checker, ResponseSet
from .checkotp import OTPRequest
from .checkvalhalla import ValhallaRequest
from .checkgoogle import GoogleRequest
from .tripmatcher import TripMatcher
from .util import *

def main():
    parser = argparse.ArgumentParser(description='Make requests to multiple routing engines and compare the results')
    parser.add_argument('testfile', help='Test GeoJSON input file')
    parser.add_argument('outfile', help='GeoJSON output file')
    parser.add_argument('modes', nargs='+')
    parser.add_argument('--when', help='Override all trip date/times, e.g. "next monday at 10am"')
    parser.add_argument('--whentz', help='Timezone for --when')
    parser.add_argument('-v', '--verbose', help='Print urls and failures', action='store_true')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    # Select planner
    request_factories = []
    i = 0
    while i < len(args.modes):
        mode = args.modes[i]
        url = args.modes[i+1]
        request_cls = Request.get_cls(mode)
        request_factories.append(functools.partial(request_cls, url))
        i += 2

    # Set log level
    level = logging.WARNING
    if args.debug:
        level = logging.DEBUG
    elif args.verbose:
        level = logging.INFO
    logging.basicConfig(format='%(message)s', level=level)

    # Load tests
    checker = Checker(request_factories=request_factories, when=args.when, whentz=args.whentz)
    checker.load(args.testfile)
    checker.run()
    fc = checker.result_geojson()
    with open(args.outfile, 'w') as f:
        json.dump(fc, f)

if __name__ == "__main__":
    main()