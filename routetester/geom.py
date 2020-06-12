# approximate
# https://stackoverflow.com/questions/4913349/
from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def haversine_feature(o, d):
    return haversine(
        o['geometry']['coordinates'][0],
        o['geometry']['coordinates'][1],
        d['geometry']['coordinates'][0],
        d['geometry']['coordinates'][1]
    )
