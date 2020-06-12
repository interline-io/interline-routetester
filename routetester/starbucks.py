import os
import sys
import json
import argparse

from .generate_od import *

def main():
    parser = argparse.ArgumentParser(description='Generate OD features from Starbucks locations or a GeoJSON file of points of interest')
    parser.add_argument('outfile', help='Output GeoJSON')
    parser.add_argument('--infile', help='Input GeoJSON')
    parser.add_argument('--origins', help='Number of origins', default=10, type=int)
    parser.add_argument('--destinations', help='Number of destinations for each origin', default=10, type=int)
    parser.add_argument('--mindistance', help='Minimum distance between origins/destinations (in kilometers)', default=0.1, type=float)
    parser.add_argument('--maxdistance', help='Minimum distance between origins/destinations (in kilometers)', default=100, type=float)
    parser.add_argument('--bbox', help='bbox', default='-180,-90,180,90')
    args = parser.parse_args()

    infile = args.infile or os.path.join(os.path.split(__file__)[0], "data", "starbucks.geojson")
    with open(infile) as f:
        data = json.load(f)

    bbox = map(float, args.bbox.split(','))
    features = bbox_filter(bbox, data['features'])
    od = generate_od(features, sample1=args.origins, sample2=args.destinations, min_distance=args.mindistance, max_distance=args.maxdistance)
    fc = generate_geojson(od)
    with open(args.outfile, 'w', encoding="utf-8") as f:
        # print(fc)
        json.dump(fc, f)


if __name__ == "__main__":
    main()

