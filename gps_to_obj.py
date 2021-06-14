import untangle #https://github.com/stchris/untangle
import argparse
#import json
import os.path

parser = argparse.ArgumentParser(description="Naively convert position and time data from a GPX file to 3D positions and time since start.")
parser.add_argument('source', help="The GPX file to process")
parser.add_argument('destination', help="The OBJ file for output")
args = parser.parse_args()


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


obj = untangle.parse(args.source)

start = obj.gpx.metadata.time.cdata
#print('start time:', start)

points = ['g']
# Grab the data from each recorded point
for point in obj.gpx.trk.trkseg.trkpt:
    points.append('\nv ' + point['lat'] + ' ' + point['lon'] + ' ' + point.ele.cdata + ' ')


with open(os.path.realpath(args.destination), 'w') as out_file:
    out_file.writelines(points)
