import gpxpy
import gpxpy.gpx
import glob, os, sys

# split segments to new files
# -------------------------
if sys.argv[1] :
    file_name = sys.argv[1]
else:
    print("please provide .gpx file for spliting")
    #file_name = (glob.glob("*.gpx")[0])

gpx_file = open(file_name, 'r')

gpxo = gpxpy.parse(gpx_file)

for track in gpxo.tracks:
    for segment_no, segment in enumerate(track.segments):
        new_file = "segment_{0}_from_{1}".format(segment_no+1,file_name)
        gpx_new = open(new_file, 'w')

        gpx = gpxpy.gpx.GPX()

        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        for point in segment.points:
            # Create points:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point.latitude, point.longitude, elevation=point.elevation,time=point.time)) 

        gpx_new.writelines(gpx.to_xml())
        gpx_new.close()

