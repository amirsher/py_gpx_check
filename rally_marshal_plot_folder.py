#!/usr/bin/python
# http://www.trackprofiler.com/gpxpy/index.html
import gpxpy
import gpxpy.gpx
import math
import sys
import csv
import glob, os
import datetime
import matplotlib.pyplot as plt
import folium
from folium.plugins import FloatImage
#from folium.plugins import MeasureControl

# python rally_marshal_folder.py 45.48612,5.909551 45.49593,5.90369 45.50341,5.90479 45.51386,5.90625
# lat,lon

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
                
                    latitude.append( point.latitude )
                    longitude.append( point.longitude )
                    foliumpoints.append(tuple([point.latitude, point.longitude]))

            if segment_no > 0 :
                output1="\nWARNING!, file {0} contain {1} segments, should be no more then 1 segment to get correct results\n".format(file,segment_no+1)
                print(output1)
                marshalfile.write("{0}\n".format(output1))

    if line_points == "line" :
        folium.features.PolyLine(foliumpoints, color="{}".format(color),popup="{}".format(file), weight=3, opacity=1).add_to(my_map)

 #       plt.axis('equal')
    plt.plot(longitude,latitude,label=file,) #
    plt.legend()
    plt.show(block=False)
    return my_map


def FindClosestSingle(i):
    marshal_point = i.split(',') # lat,lon
    marshal_point[0] = float(marshal_point[0])
    marshal_point[1] = float(marshal_point[1])
    
    closest_to_marshal_point = None
    closest_to_marshal_point_meters = 100000000000000000000.

    reader = csv.reader(open("{1}/zzz_{0}.csv".format(file,cwd)), delimiter=',')
    for row in reader:

        # calculate the distance to the marshal
#                    start_meters = distance_haversine(marshal_point, (float(row[1]),float(row[2])))

        start_meters = distance_vincenty(marshal_point, (float(row[1]),float(row[2])))

        # determine if point closest to marshal
        if start_meters < closest_to_marshal_point_meters  :
            closest_to_marshal_point = row[0]
            closest_to_marshal_point_meters = round(start_meters,2)

    return (closest_to_marshal_point,closest_to_marshal_point_meters)

 
def OutputMarshal(x,closest_to_marshal_point,closest_to_marshal_point_meters,out_of_range):
    
    reader = csv.reader(open("{1}/zzz_{0}.csv".format(file,cwd)), delimiter=',')
    for row in reader:
            if (int(row[0]) == int(closest_to_marshal_point)) :
                if int(closest_to_marshal_point_meters) > int(out_of_range) :
                    output = ("Passed Marshal {0} at {1} distance of {2} meters and speed of {3} kph. OUT OF RANGE".format(x, row[4],int(closest_to_marshal_point_meters), row[3]))
                else :
                    output = ("Passed Marshal {0} at {1} distance of {2} meters and speed of {3} kph.".format(x, row[4],int(closest_to_marshal_point_meters), row[3]))
                print(output)
                marshalfile.write("{}\n".format(output))
                folium.features.Circle(location=(float(row[1]),float(row[2])),radius=5,stroke=False,fill="true",color="black",fill_color="black", popup="{0}<br>passed {1} meters from marshal {2}".format(file,closest_to_marshal_point_meters,x),fill_opacity=1).add_to(my_map)


#['red', 'blue', 'green', 'purple', 'orange', 'darkred','lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue','darkpurple', 'white', 'pink', 'lightblue', 'lightgreen','gray', 'black', 'lightgray']

color = [ "red", "blue", "green", "yellow", "purple", "orange", "brown", "palegreen", "indigo", "aqua", "brick", "emeraldgreen", "lightred", "gray", "white", "black" ]
c = 0

now = datetime.datetime.now() 
distance_to_marshal_allowed = 80
cwd = os.getcwd()

line_points = "line" # display "line" or "points", points is very slow.

if line_points != "line" and line_points != "points":
    line_points = "line"

with open("{0}/zzz_marshal_results.txt".format(cwd), "w"): pass # clear the txt file

with open("{0}/zzz_marshal_results.txt".format(cwd), "a") as marshalfile:

    MarshalPoints= int(len(sys.argv)-1)

    output = ("File generated on {2}.\nThere are {0} Marshal Point(s).\nOut of range set to {1} meters.\n".format(MarshalPoints,distance_to_marshal_allowed,now.strftime("%Y-%m-%d %H:%M:%S")))
    print("\n{}".format(output))
    marshalfile.write("{}\n".format(output))

    if isinstance(MarshalPoints, int) :
        
        if (glob.glob("*.gpx")) :
            my_map=foliumMap(glob.glob("*.gpx")[0])
        else:
            print("No gpx files\n")
            sys.exit(0)
        #os.chdir("/mydir")
        for file in glob.glob("*.gpx"):
                            
            print(file)
            my_map=ConvertAndSpeed(file,my_map,color[c],line_points)
            marshalfile.write("{}\n".format(file))
            for x in range(1, MarshalPoints+1):
                marshal = FindClosestSingle((sys.argv)[x])

                # add marshal marker to web map
                marshalpoint = ((sys.argv)[x]).split(',')
                marshalpoint[0] = float(marshalpoint[0])
                marshalpoint[1] = float(marshalpoint[1])
                
                folium.Marker(location=(marshalpoint[0],marshalpoint[1]),icon=folium.Icon(color='blue', icon='male', prefix="fa"), popup="Marshal {0}<br>{1} , {2}".format(x,marshalpoint[0],marshalpoint[1])).add_to(my_map)
                
                folium.features.Circle(location=(marshalpoint[0],marshalpoint[1]),radius=distance_to_marshal_allowed, weight=1,color="gray", popup="allowed {0} meters from marshal {1}".format(distance_to_marshal_allowed,x),opacity=0.2).add_to(my_map)

                OutputMarshal(x,marshal[0],marshal[1],distance_to_marshal_allowed)



            os.remove("{1}/zzz_{0}.csv".format(file,cwd))
            if c < 15 :
                c = c + 1
            else:
                c = 0
            
        my_map.save("TrackingMap.html")

    else:
        print('\nworong arguments, please use:\n\npython rally_marshal_folder.py marshal1_lat,marshal1_long marshal2_lat,marshal2_long \n\nEx: python rally_marshal_folder.py 45.48612,5.909551 45.49593,5.90369 45.50341,5.90479 45.51386,5.90625\n')
        sys.exit(0)

marshalfile.close()

plt.xlabel('latitude')
plt.ylabel('longitude')
plt.savefig('tracking.png', bbox_inches='tight', dpi=288)
plt.title(u'\u25B2 \nN ',loc='left', rotation = 0,family='sans-serif', fontsize=16) # north arrow
plt.tight_layout()
plt.show()
