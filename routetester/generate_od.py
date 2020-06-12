#!/usr/bin/env python
import sys
import os
import json
import random

MIN_DISTANCE = 0.1
MAX_DISTANCE = 10.0
MAX_SAMPLE = 10000

from .geom import haversine, haversine_feature

def bbox_filter(bbox, features):
    # simple bbox test
    left, bottom, right, top = bbox
    return [
        i for i in features 
        if left <= i['geometry']['coordinates'][0] <= right and bottom <= i['geometry']['coordinates'][1] <= top
    ]

def generate_od(features, sample1=None, sample2=None, min_distance=MIN_DISTANCE, max_distance=MAX_DISTANCE):
    # find and sample od pairs
    sample1 = sample1 or len(features)
    sample2 = sample2 or len(features)
    pairs = []
    for o in random.sample(features, min(sample1, len(features), MAX_SAMPLE)):
        # d = sorted(features, key=lambda d:haversine_feature(o,d) )
        # pairs.append([o,d])
        p = [[o,d] for d in features if min_distance <= haversine_feature(o,d) <= max_distance]
        pairs += random.sample(p, min(sample2, len(p), MAX_SAMPLE))
    return pairs

def generate_geojson(od):
    # write output
    features = []
    for o,d in od:
        features.append({
            "type": "Feature",
            "properties": {
                "title": "%s -> %s"%(
                    o['properties']['title'], 
                    d['properties']['title'], 
                ),
                "distance": haversine_feature(o, d),
                "stroke": "#000ad3",
                "stroke-width": "2.0",
                "stroke-opacity": 1,
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    o['geometry']['coordinates'],
                    d['geometry']['coordinates'],
                ]
            }
        })
    features = sorted(features, key=lambda x:x['properties']['distance'])
    return {
        "type": "FeatureCollection",
        "features": features
    }

