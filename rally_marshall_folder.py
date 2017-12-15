#!/usr/bin/python
# http://www.trackprofiler.com/gpxpy/index.html
import gpxpy
import gpxpy.gpx
import math
import sys
import csv
import glob, os
import datetime
    
# python rally_marshall_folder.py 45.48612,5.909551 45.49593,5.90369 45.50341,5.90479 45.51386,5.90625
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


def ConvertAndSpeed (file):
    with open("{1}/zzz_{0}.csv".format(file,cwd), "w"): pass # clear the csv file

    with open("{0}".format(file), "r") as gpx_file: 

    #gpx_file = open('z20171214-111736.gpx', 'r')

        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point_no, point in enumerate(segment.points):
                    # calculate the speed
                    if point.speed != None:
                        speed = round((point.speed)*3.6,2)
                    elif point_no > 0 and point_no < len(segment.points)-1  :
                        speed1 = point.speed_between(segment.points[point_no - 1])
                        speed2 = point.speed_between(segment.points[point_no + 1])
                        if (speed1 is None) or (speed2 is None) :
                            pass
                        else:
                            speed = round(((speed1+speed2)/2)*3.6,2) #speed im kph rounded to 2 decimal
                    else :
                        speed = 0.0
                            
                    with open("{1}/zzz_{0}.csv".format(file,cwd), "a") as gpxfile:

                        gpxfile.write('{0},{1},{2},{3},{4}\n'.format(point_no, point.latitude, point.longitude, speed, point.time))
                        gpxfile.close()
    

def FindClosestSingle(i):
    marshall_point = i.split(',') # lat,lon
    marshall_point[0] = float(marshall_point[0])
    marshall_point[1] = float(marshall_point[1])
    
    closest_to_marshall_point = None
    closest_to_marshall_point_meters = 100000000000000000000.

    reader = csv.reader(open("{1}/zzz_{0}.csv".format(file,cwd)), delimiter=',')
    for row in reader:

        # calculate the distance to the marshall
#                    start_meters = distance_haversine(marshall_point, (float(row[1]),float(row[2])))

        start_meters = distance_vincenty(marshall_point, (float(row[1]),float(row[2])))

        # determine if point closest to marshall
        if start_meters < closest_to_marshall_point_meters  :
            closest_to_marshall_point = row[0]
            closest_to_marshall_point_meters = round(start_meters,2)

    return (closest_to_marshall_point,closest_to_marshall_point_meters)

 
def OutputMarshall(x,closest_to_marshall_point,closest_to_marshall_point_meters,out_of_range):
    
    reader = csv.reader(open("{1}/zzz_{0}.csv".format(file,cwd)), delimiter=',')
    for row in reader:
            if (int(row[0]) == int(closest_to_marshall_point)) :
                if int(closest_to_marshall_point_meters) > int(out_of_range) :
                    output = ("Passed Marshall {0} at {1} range of {2} meters and speed of {3} kph. OUT OF RANGE".format(x, row[4],int(closest_to_marshall_point_meters), row[3]))
                else :
                    output = ("Passed Marshall {0} at {1} range of {2} meters and speed of {3} kph.".format(x, row[4],int(closest_to_marshall_point_meters), row[3]))
                print(output)
                marshallfile.write("{}\n".format(output))

now = datetime.datetime.now() 
range_to_marshall_allowed = 80
cwd = os.getcwd()

with open("{0}/zzz_marshall_results.txt".format(cwd), "w"): pass # clear the txt file

with open("{0}/zzz_marshall_results.txt".format(cwd), "a") as marshallfile:

    MarshallPoints= int(len(sys.argv)-1)

    output = ("File generated on {2}.\nThere are {0} Marshall Points.\nOut of range set to {1} meters.\n".format(MarshallPoints,range_to_marshall_allowed,now.strftime("%Y-%m-%d %H:%M:%S")))
    print("\n{}".format(output))
    marshallfile.write("{}\n".format(output))

    if isinstance(MarshallPoints, int) :

        #os.chdir("/mydir")
        for file in glob.glob("*.gpx"):
                            
            ConvertAndSpeed (file)
            print(file)
            marshallfile.write("{}\n".format(file))
            for x in range(1, MarshallPoints+1):
                marshall = FindClosestSingle((sys.argv)[x])
                OutputMarshall(x,marshall[0],marshall[1],range_to_marshall_allowed)


    else:
        print('\nworong arguments, please use:\n\npython rally_marshall_folder.py marshall1_lat,marshall1_long marshall2_lat,marshall2_long \n\nEx: python rally_marshall_folder.py 45.48612,5.909551 45.49593,5.90369 45.50341,5.90479 45.51386,5.90625\n')
        sys.exit(0)

marshallfile.close()
