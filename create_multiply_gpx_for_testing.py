import gpxpy
import gpxpy.gpx
from random import randint
import glob, os

# takes the firs .gpx file and multiply it with a little devation
# -------------------------
file_name = (glob.glob("*.gpx")[0])
gpx_file = open(file_name, 'r')

gpxo = gpxpy.parse(gpx_file)

for x in range(1, 10):
    new_file = "new{0}_{1}".format(x,file_name)

    gpx_new = open(new_file, 'w')


    gpx = gpxpy.gpx.GPX()

    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    # Create first segment in our GPX track:
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    for track in gpxo.tracks:
        for segment in track.segments:
            for point_no, point in enumerate(segment.points):
                # Create points:
                if point_no % 3 == 0 : # cut the number of points to third
                    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point.latitude+(randint(-5, 5)/10000), point.longitude+(randint(-5, 5)/10000), elevation=point.elevation,time=point.time)) #100m deviation
    #               gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point.latitude+(randint(-5, 5)/100000), point.longitude+(randint(-5, 5)/100000), elevation=point.elevation,time=point.time)) #10m deviation
    gpx_new.writelines(gpx.to_xml())
    gpx_new.close()

