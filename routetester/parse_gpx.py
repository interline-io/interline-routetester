import glob
import gpxpy
import gpxpy.gpx

def read_gpx(filename):
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)
    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    'lat': point.latitude,
                    'lon' : point.longitude
                })
    return points

def read_sample_gpx_files():
    points_in_files = {}
    for filename in glob.glob('sample-gpx-files/*.gpx'):
        points_in_files[filename] = read_gpx(filename)
    return points_in_files