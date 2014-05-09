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

fh = open(r'C:\Users\thartley\Documents\LocationHistory5_1_14.json')
buf = fh.read()
raw = json.loads(buf)
fh.close()

ld = pd.DataFrame(raw['locations'])
ld['latitudeE7'] = ld['latitudeE7']/float(1e7)
ld['longitudeE7'] = ld['longitudeE7']/float(1e7)

# <codecell>

point = Point.from_google_latitude(raw['locations'][1])
point.date

# <codecell>

fpoints = [Point.from_google_latitude(p) for p in raw['locations'][:1900]]
plt.plot([point.lon for point in points], [point.lat for point in points], 'b.-')

# <headingcell level=1>

# Plot ERI Shapefile

# <codecell>

import fiona
from itertools import chain
from mpl_toolkits.basemap import Basemap
import pandas as pd
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
from shapely.prepared import prep

# <codecell>

#shp = fiona.open(r'C:\Users\thartley\Documents\Seattle_20City_20Limits\WGS84\Seattle City Limits')
#r'C:\Users\thartley\Downloads\london\london_wards'
shapefile = r'C:\Users\thartley\Downloads\Neighborhoods\WGS84\Neighborhoods'

shp = fiona.open(shapefile+'.shp')
bds = shp.bounds
shp.close()
extra = 0.01
ll = (bds[0], bds[1])
ur = (bds[2], bds[3])
coords = list(chain(ll, ur))
w, h = coords[2] - coords[0], coords[3] - coords[1]

# <codecell>

m = Basemap(
    projection='tmerc',
    lon_0=-122.3,
    lat_0=47.6,
    #lon_0=-2.,
    #lat_0=49.,
    ellps = 'WGS84',
    llcrnrlon=coords[0] - extra * w,
    llcrnrlat=coords[1] - extra + 0.01 * h,
    urcrnrlon=coords[2] + extra * w,
    urcrnrlat=coords[3] + extra + 0.01 * h,
    lat_ts=0,
    resolution='i',
    suppress_ticks=True)
out = m.readshapefile(
    #r'C:\Users\thartley\Documents\Seattle_20City_20Limits\WGS84\Seattle City Limits',
    shapefile,
    'seattle',
    color='none',
    zorder=2)

# <codecell>

# Plot all neighborhoods
fig = plt.figure(figsize=(8,12))
for nhood in m.seattle:
    plt.plot([xx[0] for xx in nhood], [xx[1] for xx in nhood], 'b')

# <codecell>

m.seattle_info[60]['L_HOOD']

# <codecell>

# set up a map dataframe
df_map = pd.DataFrame({
    'poly': [Polygon(xy) for xy in m.seattle],
    'name': })
df_map['area_m'] = df_map['poly'].map(lambda x: x.area)
df_map['area_km'] = df_map['area_m'] / 100000

# <codecell>

# Create Point objects in map coordinates from dataframe lon and lat values
map_points = pd.Series(
    [Point(m(mapped_x, mapped_y)) for mapped_x, mapped_y in zip(ld['longitudeE7'], 
                                                                ld['latitudeE7'])])
plaque_points = MultiPoint(list(map_points.values))
wards_polygon = prep(MultiPolygon(list(df_map['poly'].values)))
# calculate points that fall within the London boundary
ldn_points = filter(wards_polygon.contains, plaque_points)

# <codecell>


