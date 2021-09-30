import untangle #https://github.com/stchris/untangle
import argparse
import math
#import json
import os.path

parser = argparse.ArgumentParser(description="Naively convert position and time data from a GPX file to 3D positions and time since start.")
parser.add_argument('source', help="The GPX file to process")
parser.add_argument('destination', help="The OBJ file for output")
args = parser.parse_args()

EARTH_RAD = 6378.8 # in km

# def elapsedTime(start, current):
#     """Return seconds elapsed from the start time to the current time. (Ignoring the year, month, and day for now because no ride that I care about lasts more than an hour or so.)"""
#
#     start = start.strip('Z')
#     current = current.strip('Z')
#     start_day, start_time = start.split('T')
#     current_day, current_time = current.split('T')
#
#     start_hour, start_minute, start_second = start_time.split(':')
#     current_hour, current_minute, current_second = current_time.split(':')
#
#     start_hour = int(start_hour)
#     start_minute = int(start_minute)
#     start_second = int(start_second)
#     current_hour = int(current_hour)
#     current_minute = int(current_minute)
#     current_second = int(current_second)
#
#     elapsed = current_second - start_second + \
#               ((current_minute - start_minute) * 60) + \
#               ((current_hour - start_hour) * 60 * 60)
#
#     return elapsed

def naive_conversion(gpx_obj):
    """Moving the lat, lon, elevation data directly to point data

        gpx_obj (xml object) : point data from gps in gpx format

        returns : point array in the format of [[lat, lon, elevation], ... ]
    """
    # Grab the data from each recorded point
    points=[]
    for point in gpx_obj.gpx.trk.trkseg.trkpt:
        points.append([point['lat'], point['lon'], point.ele.cdata])
    return points


def spherical_conversion(gpx_obj):
    """Plot the points directly onto an Earth-sized sphere by projecting
        lat and lon onto a sphere and then converting to cartesian space.

        gpx_obj (xml object) : point data from gps in gpx format

        returns : point array in the format of [[x, y, z], ... ]
    """
    points=[]
    for point in gpx_obj.gpx.trk.trkseg.trkpt:
        #plot on a sphere
        theta = math.radians(float(point['lon']))
        phi = math.radians(float(point['lat']))
        #convert elevation data to km and add to radius of Earth
        rho = EARTH_RAD + float(point.ele.cdata)/1000.

        # convert to cartesian
        x_pt = rho * math.sin(phi) * math.cos(theta)
        y_pt = rho * math.sin(phi) * math.cos(phi)
        z_pt = rho * math.cos(phi)

        points.append([x_pt, y_pt, z_pt])
    return points


def mercator_conversion(gpx_obj):
    """Mercator projection of the lat and lon, placing the start point
        at 0,0,0.

        gpx_obj (xml object) : point data from gps in gpx format

        returns : point array in the format of [[x, y, z], ... ]
    """
    points=[]
    # get start point
    offset_lon = float(gpx_obj.gpx.trk.trkseg.trkpt[0]['lon'])
    offset_lat = float(gpx_obj.gpx.trk.trkseg.trkpt[0]['lat'])
    offset_ele = float(gpx_obj.gpx.trk.trkseg.trkpt[0].ele.cdata)

    for point in gpx_obj.gpx.trk.trkseg.trkpt:
        x_pt = (float(point['lon'])-offset_lon) / (math.pi) * EARTH_RAD

        lat = float(point['lat'])-offset_lat
        z_pt = math.log( (1+math.sin(lat))/(1-math.sin(lat))) / (-2*math.pi) * EARTH_RAD
        # convert to km
        #y_pt = float(point.ele.cdata)/1000.
        # but dividing by 20 just looks better
        y_pt = (float(point.ele.cdata)-offset_ele)/20.
        points.append([x_pt, y_pt, z_pt])
    return points


def write_obj(points, write_path):
    """write out an obj file

        points (array) : converted point data
        write_path (string) : path to file

        returns : None
    """
    obj_out = ['g']
    for point in points:
        str_point = [str(n) for n in point]
        obj_out.append('\nv ' + ' '.join(str_point))

    with open(os.path.realpath(write_path), 'w') as out_file:
        out_file.writelines(obj_out)


if __name__ == '__main__':
    gpx_obj = untangle.parse(args.source)

    #naive_points = naive_conversion(gpx_obj)
    #write_obj(gpx_points, args.destination)

    #spherical_points = spherical_conversion(gpx_obj)
    #write_obj(spherical_points, args.destination)

    mercator_points = mercator_conversion(gpx_obj)
    write_obj(mercator_points, args.destination)

    #start = obj.gpx.metadata.time.cdata
    #print('start time:', start)
