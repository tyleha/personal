# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%load_ext grasp

import json
import time
import matplotlib.pyplot as plt

# <codecell>

import math
from functools import total_ordering
import datetime

@total_ordering
class Point(object):
    def __init__(self, lat, lon, time, accuracy=None):
        self.lat = lat
        self.lon = lon
        self.time = time
        self.accuracy = accuracy
        
        self.date = datetime.datetime.fromtimestamp(self.time)
        
    def __repr__(self):
        return "Point(%s, %s, %s)"%(self.lat, self.lon, self.time)     

    def __lt__(self, other):
        return self.time < other.time
    
    def __eq__(self, other):
        return self.time == other.time
    
    def distance_between(self, other):
        return distance_on_unit_sphere(self.lat, self.lon, 
                                       other.lat, other.lon) & 3959. #radius of earth in miles
    
    @classmethod
    def from_google_latitude(cls, latitude_dict):
        return cls(float(latitude_dict['latitudeE7'])/1e7, 
                     float(latitude_dict['longitudeE7'])/1e7, 
                     int(latitude_dict['timestampMs'])/1000.,
                     accuracy=latitude_dict['accuracy'])    
    
def distance_on_unit_sphere(lat1, long1, lat2, long2):
    # http://www.johndcook.com/python_longitude_latitude.html
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0  
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc

# <codecell>

fh = open(r'C:\Users\thartley\Documents\Dropbox\LocationHistory5_1_14.json')
buf = fh.read()
raw = json.loads(buf)

# <codecell>

point = Point.from_google_latitude(raw['locations'][1])
point.date

# <codecell>

points = [Point.from_google_latitude(p) for p in raw['locations'][:1900]]
plt.plot([point.lon for point in points], [point.lat for point in points], 'b.-')

# <headingcell level=1>

# Plot ERI Shapefile

# <codecell>

import fiona

# <codecell>


shp = fiona.open('data/london_wards.shp')
bds = shp.bounds
shp.close()
extra = 0.01
ll = (bds[0], bds[1])
ur = (bds[2], bds[3])
coords = list(chain(ll, ur))
w, h = coords[2] - coords[0], coords[3] - coords[1]

