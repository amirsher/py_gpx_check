#!/usr/bin/python
# http://www.trackprofiler.com/gpxpy/index.html
import gpxpy
import gpxpy.gpx
import math
import sys
import csv
import glob, os
import datetime
import folium
from folium.plugins import FloatImage
#from folium.plugins import MeasureControl

# python rally_speeding_folder.py 45.49222,5.90380 45.49885,5.90372 70 45.49222,5.90380 45.49885,5.90372 70

#restricted_start = (32.49222,34.90380) # lat,lon
#restricted_finish = (32.49885,34.90372) # lat,lon
#restricted_speed = 70 # kph

# WGS 84
a = 6378137  # meters
f = 1 / 298.257223563
b = 6356752.314245  # meters; b = (1 - f)a

MILES_PER_KILOMETER = 0.621371

MAX_ITERATIONS = 200
CONVERGENCE_THRESHOLD = 1e-12  # .000,000,000,001

def distance_vincenty(point1, point2):
    """
    Vincenty's formula (inverse method) to calculate the distance (in
    kilometers or miles) between two points on the surface of a spheroid
    """

    # short-circuit coincident points
    if point1[0] == point2[0] and point1[1] == point2[1]:
        return 0.0

    U1 = math.atan((1 - f) * math.tan(math.radians(point1[0])))
    U2 = math.atan((1 - f) * math.tan(math.radians(point2[0])))
    L = math.radians(point2[1] - point1[1])
    Lambda = L

    sinU1 = math.sin(U1)
    cosU1 = math.cos(U1)
    sinU2 = math.sin(U2)
    cosU2 = math.cos(U2)

    for iteration in range(MAX_ITERATIONS):
        sinLambda = math.sin(Lambda)
        cosLambda = math.cos(Lambda)
        sinSigma = math.sqrt((cosU2 * sinLambda) ** 2 +
                             (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
        if sinSigma == 0:
            return 0.0  # coincident points
        cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
        sigma = math.atan2(sinSigma, cosSigma)
        sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
        cosSqAlpha = 1 - sinAlpha ** 2
        try:
            cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
        except ZeroDivisionError:
            cos2SigmaM = 0
        C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha))
        LambdaPrev = Lambda
        Lambda = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma *
                                               (cos2SigmaM + C * cosSigma *
                                                (-1 + 2 * cos2SigmaM ** 2)))
        if abs(Lambda - LambdaPrev) < CONVERGENCE_THRESHOLD:
            break  # successful convergence
    else:
        return None  # failure to converge

    uSq = cosSqAlpha * (a ** 2 - b ** 2) / (b ** 2)
    A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
    B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
    deltaSigma = B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma *
                 (-1 + 2 * cos2SigmaM ** 2) - B / 6 * cos2SigmaM *
                 (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2SigmaM ** 2)))
    s = b * A * (sigma - deltaSigma)

#    s /= 1000  # meters to kilometers
    return round(s, 6)

def distance_haversine(point1, point2):    
    R=6371009                               # radius of Earth in meters
    phi_1=math.radians(point2[0])
    phi_2=math.radians(point1[0])

    delta_phi=math.radians(point1[0]-point2[0])
    delta_lambda=math.radians(point1[1]-point2[1])

    a=math.sin(delta_phi/2.0)**2+\
    math.cos(phi_1)*math.cos(phi_2)*\
    math.sin(delta_lambda/2.0)**2
    c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    
    meters=R*c                         # output distance in meters
    #kms=meters/1000.0              # output distance in kilometers
    #miles=meters*0.000621371      # output distance in miles
    #feet=miles*5280               # output distance in feet
    return meters


def foliumMap(file):
    foliumpoints = [] # for folium
    with open("{0}".format(file), "r") as gpx_file: 
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point_no, point in enumerate(segment.points):
                       foliumpoints.append(tuple([point.latitude, point.longitude]))
    ave_lat = sum(p[0] for p in foliumpoints)/len(foliumpoints)
    ave_lon = sum(p[1] for p in foliumpoints)/len(foliumpoints)
    # Load map centred on average coordinates
    #Map tileset to use. Can choose from this list of built-in tiles:
    #            - "OpenStreetMap"
    #            - "Stamen Terrain", "Stamen Toner", "Stamen Watercolor"
    #            - "CartoDB positron", "CartoDB dark_matter"
    #            - "Mapbox Bright", "Mapbox Control Room" (Limited zoom)
    #            - "Cloudmade" (Must pass API key)
    #            - "Mapbox" (Must pass API key)

    my_map = folium.Map(location=[ave_lat, ave_lon], zoom_start=12,control_scale=True, tiles='OpenStreetMap')
    url = ('http://tnuatiming.com/android-chrome-36x36.png')
    FloatImage(url, bottom=2, left=96).add_to(my_map)
    #    my_map.add_child(MeasureControl())

    return my_map


def ConvertAndSpeed (file,my_map,color,line_points):
    with open("{1}/zzz_{0}.csv".format(file,cwd), "w"): pass # clear the csv file

    with open("{0}".format(file), "r") as gpx_file: 

    #gpx_file = open('z20171214-111736.gpx', 'r')
        latitude = [] # for matplotlib
        longitude = [] # for matplotlib
        foliumpoints = [] # for folium

        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment_no, segment in enumerate(track.segments):
                for point_no, point in enumerate(segment.points):
                    # calculate the speed
                    if point.speed != None:
                        speed = round((point.speed)*3.6,2) #convert to kph rounded to 2 decimal
#                    elif point_no > 0 and point_no < len(segment.points)-1  :
#                        speed1 = point.speed_between(segment.points[point_no - 1])
#                        speed2 = point.speed_between(segment.points[point_no + 1])
#                        if (speed1 is None) or (speed2 is None) :
#                            pass
#                        else:
#                           speed = round(((speed1+speed2)/2)*3.6,2) #speed im kph rounded to 2 decimal
                    else :
#                        speed = 0.0
                        speed = segment.get_speed(point_no)
                        if speed != None:
                            speed = round(speed*3.6,2) #convert to kph rounded to 2 decimal

                    if line_points == "points" :
                        folium.features.Circle(location=(point.latitude,point.longitude),radius=5,stroke=False,fill="true",color="{}".format(color),fill_color="{}".format(color), popup="{0}<br>speed: {1} kph<br>{4}<br>{2} , {3}".format(file,speed,point.latitude,point.longitude,point.time),fill_opacity=0.8).add_to(my_map)
                            


                    with open("{1}/zzz_{0}.csv".format(file,cwd), "a") as gpxfile:

                        gpxfile.write('{0},{1},{2},{3},{4}\n'.format(point_no, point.latitude, point.longitude, speed, point.time))
                        gpxfile.close()
                
                    if line_points == "line" :
                        latitude.append( point.latitude )
                        longitude.append( point.longitude )
                        foliumpoints.append(tuple([point.latitude, point.longitude]))

            if segment_no > 0 :
                output1="\nWARNING!, file {0} contain {1} segments, should be no more then 1 segment to get correct results\n".format(file,segment_no+1)
                print(output1)
                speddingfile.write("{0}\n".format(output1))

    if line_points == "line" :
        folium.features.PolyLine(foliumpoints, color="{}".format(color),popup="{}".format(file), weight=3, opacity=1).add_to(my_map)
    return my_map

def FindClosest(i):
    restricted_start = sys.argv[(i*3)-2].split(',') # lat,lon
    restricted_start[0] = float(restricted_start[0])
    restricted_start[1] = float(restricted_start[1])
    
    restricted_finish = sys.argv[(i*3)-1].split(',') # lat,lon
    restricted_finish[0] = float(restricted_finish[0])
    restricted_finish[1] = float(restricted_finish[1])

    restricted_speed = float(sys.argv[i*3]) # kph

    closest_to_start = None
    closest_to_start_meters = 100000000000000000000.
    closest_to_finish = None
    closest_to_finish_meters = 100000000000000000000.

    reader = csv.reader(open("{1}/zzz_{0}.csv".format(file,cwd)), delimiter=',')
    for row in reader:

        # calculate the distance to the restricted zone start
#                    start_meters = distance_haversine(restricted_start, (float(row[1]),float(row[2])))

        # calculate the distance to the restricted zone finish
#                    finish_meters = distance_haversine(restricted_finish, (float(row[1]),float(row[2])))

        start_meters = distance_vincenty(restricted_start, (float(row[1]),float(row[2])))
        finish_meters = distance_vincenty(restricted_finish, (float(row[1]),float(row[2])))

        # determine if point closest to start or finish
        if start_meters < closest_to_start_meters  :
            closest_to_start = row[0]
            closest_to_start_meters = round(start_meters,2)
        if finish_meters < closest_to_finish_meters  :
            closest_to_finish = row[0]
            closest_to_finish_meters = round(finish_meters,2)

    output = ('\n{4}\nRestricted {6} kph Zone {5}:\nClosest to start Point {0} at {1} meters, Closest to finish Point {2} at {3} meters.\n'.format(closest_to_start, closest_to_start_meters, closest_to_finish, closest_to_finish_meters, file,i,restricted_speed))
    print(output)
    speddingfile.write("{0}\n".format(output))
    folium.Marker(location=(restricted_start[0],restricted_start[1]),icon=folium.Icon(color='red', icon='exclamation', prefix='fa'), popup="restricted zone {0} start<br>speed limit <b>{1} kph</b>".format(i,restricted_speed)).add_to(my_map)
    folium.Marker(location=(restricted_finish[0],restricted_finish[1]),icon=folium.Icon(color='green', icon='check', prefix='fa'), popup="restricted zone {0} end".format(i)).add_to(my_map)

    return (closest_to_start,closest_to_finish,restricted_speed)
    
    
def OutputSpedding(closest_to_start,closest_to_finish,restricted_speed):
    
    reader = csv.reader(open("{1}/zzz_{0}.csv".format(file,cwd)), delimiter=',')
    for row in reader:
        if ((int(row[0]) >= int(closest_to_start)) and (int(row[0]) <= int(closest_to_finish))  and (float(row[3]) >= int(restricted_speed))):
            output = ("SPEEDING!!! at point {0} latitude: {1} longitude: {2} speed: {3} kph.".format(row[0],row[1],row[2],row[3]))
            print(output)
            speddingfile.write("{}\n".format(output))
            folium.Marker(location=(float(row[1]),float(row[2])),icon=folium.Icon(color='black', icon='camera', prefix='fa'), popup="{0}<br>speed: <b>{1} kph</b><br>{4}<br>{2} , {3}".format(file,row[3],row[1],row[2],row[4])).add_to(my_map)


color = [ "red", "blue", "green", "yellow", "purple", "orange", "brown", "palegreen", "indigo", "aqua", "brick", "emeraldgreen", "lightred", "gray", "white", "black" ]
c = 0

now = datetime.datetime.now() 
cwd = os.getcwd()
reverse = 0

line_points = "points" # display "line" or "points", points is very slow.

if line_points != "line" and line_points != "points":
    line_points = "line"

with open("{0}/zzz_spedding_results.txt".format(cwd), "w"): pass # clear the txt file

with open("{0}/zzz_spedding_results.txt".format(cwd), "a") as speddingfile:
        
    restrictedZones= int((len(sys.argv)-1)/3)
        
    output = ("File generated on {1}.\nThere are {0} restricted Zone(s).".format(restrictedZones,now.strftime("%Y-%m-%d %H:%M:%S")))
    print("\n{}".format(output))
    speddingfile.write("{}\n".format(output))

    if isinstance(restrictedZones, int) :
        if (glob.glob("*.gpx")) :
            my_map=foliumMap(glob.glob("*.gpx")[0])
        else:
            print("No gpx files\n")
            sys.exit(0)

        #os.chdir("/mydir")
        for file in glob.glob("*.gpx"):
                            
            my_map=ConvertAndSpeed(file,my_map,color[c],line_points)

            for x in range(1, restrictedZones+1):

                zone = FindClosest(x) # number of restricted zone
                OutputSpedding(zone[0],zone[1],zone[2])
                if reverse == 1 :
                    OutputSpedding(zone[1],zone[0],zone[2])

            os.remove("{1}/zzz_{0}.csv".format(file,cwd))
            if c < 15 :
                c = c + 1
            else:
                c = 0
            
        my_map.save("SpeedingMap.html")

    else:
        print('\nworong arguments, please use:\n\npython rally_speeding_folder.py start_lat,start_long finish_lat,finish_long restricted_speed\n\nEx: python rally_speeding_folder.py 45.49222,5.90380 45.49885,5.90372 70 45.49222,5.90380 45.49885,5.90372 65\n')
        sys.exit(0)
