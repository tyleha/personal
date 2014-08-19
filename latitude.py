# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Google Latitude Analysis

# <codecell>

%load_ext grasp

import matplotlib.pyplot as plt
import numpy as np
import fiona
from itertools import chain
from mpl_toolkits.basemap import Basemap
import pandas as pd
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
from shapely.prepared import prep
import matplotlib.cm as cm
from matplotlib.collections import PatchCollection
from descartes import PolygonPatch
import json
import datetime

import helpers

# <codecell>

# Convenience functions for working with colour ramps and bars
def colorbar_index(ncolors, cmap, labels=None, **kwargs):
    """
    This is a convenience function to stop you making off-by-one errors
    Takes a standard colourmap, and discretises it,
    then draws a color bar with correctly aligned labels
    """
    cmap = cmap_discretize(cmap, ncolors)
    mappable = cm.ScalarMappable(cmap=cmap)
    mappable.set_array([])
    mappable.set_clim(-0.5, ncolors+0.5)
    colorbar = plt.colorbar(mappable, **kwargs)
    colorbar.set_ticks(np.linspace(0, ncolors, ncolors))
    colorbar.set_ticklabels(range(ncolors))
    if labels:
        colorbar.set_ticklabels(labels)
    return colorbar

def cmap_discretize(cmap, N):
    """
    Return a discrete colormap from the continuous colormap cmap.

        cmap: colormap instance, eg. cm.jet. 
        N: number of colors.

    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)

    """
    if type(cmap) == str:
        cmap = get_cmap(cmap)
    colors_i = concatenate((linspace(0, 1., N), (0., 0., 0., 0.)))
    colors_rgba = cmap(colors_i)
    indices = linspace(0, 1., N + 1)
    cdict = {}
    for ki, key in enumerate(('red', 'green', 'blue')):
        cdict[key] = [(indices[i], colors_rgba[i - 1, ki], colors_rgba[i, ki]) for i in xrange(N + 1)]
    return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d" % N, cdict, 1024)

# <codecell>

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

# <headingcell level=4>

# Load Latitude data

# <codecell>

try:
    fh = open(r'C:\Users\Tyler\Documents\My Dropbox\LocationHistory_8_18_14.json')
except:
    fh = open(r'C:\Users\thartley\Documents\Dropbox\LocationHistory_8_18_14.json')
buf = fh.read()
raw = json.loads(buf)
fh.close()

ld_full = pd.DataFrame(raw['locations'])
ld_full['latitudeE7'] = ld_full['latitudeE7']/float(1e7)
ld_full['longitudeE7'] = ld_full['longitudeE7']/float(1e7)
ld_full['timestamp'] = ld_full['timestampMs'].map(lambda x: float(x)/1000)
ld = ld_full[ld_full.timestampMs > 1374303600.0*1000] #time since Jul. 20, 2013 when data reporting increased
ld['timediff'] = ld.timestamp.diff()
ld['datetime'] = ld.timestamp.map(lambda x: datetime.datetime.fromtimestamp(x))

# <headingcell level=4>

# Get boundaries from shapefile

# <codecell>

#shp = fiona.open(r'C:\Users\thartley\Documents\Seattle_20City_20Limits\WGS84\Seattle City Limits')
#r'C:\Users\thartley\Downloads\london\london_wards'
shapefilename = helpers.user_prefix() + r'data\Neighborhoods\WGS84\Neighborhoods'
#shapefilename = helpers.user_prefix() + r'data\Shorelines\WGS84\Shorelines'

shp = fiona.open(shapefilename+'.shp')
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
    lon_0=np.mean([coords[0], coords[2]]),
    lat_0=np.mean([coords[1], coords[3]]),
    ellps = 'WGS84',
    llcrnrlon=coords[0] - extra * w,
    llcrnrlat=coords[1] - (0.08 * h), 
    urcrnrlon=coords[2] + extra * w,
    urcrnrlat=coords[3] + (extra+0.01 * h),
    resolution='i',
    suppress_ticks=True)
# Import the shapefile data to the Basemap 
out = m.readshapefile(shapefilename, 'seattle', drawbounds=False, color='none', zorder=2)


# <codecell>

# set up a map dataframe
df_map = pd.DataFrame({
    'poly': [Polygon(xy) for xy in m.seattle],
    'name': [nhood['S_HOOD'] for nhood in m.seattle_info]})
df_map['area_m'] = df_map['poly'].map(lambda x: x.area)
df_map['area_km'] = df_map['area_m'] / 100000
#df_map['poly'].append(Polygon(m2.water[0]))

# <codecell>

zzz="""
# Plot all neighborhoods
fig = plt.figure(figsize=(8,13))
for nhood in m.seattle:
    xd, yd = zip(*nhood)
    plt.plot(xd, yd)
#plt.plot(ld['latitudeE7'], ld['longitudeE7'])
plt.axis('scaled')
"""

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

helpers.tic()

figwidth = 14
fig = plt.figure(figsize=(figwidth, figwidth*h/w))
ax = fig.add_subplot(111, axisbg='w', frame_on=False)

# draw ward patches from polygons
df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(
    x, fc='#555555', ec='#555555', lw=1, alpha=1, zorder=0))
# plot boroughs by adding the PatchCollection to the axes instance
ax.add_collection(PatchCollection(df_map['patches'].values, match_original=True))

# the mincnt argument only shows cells with a value >= 1
# hexbin wants np arrays, not plain lists
hx = m.hexbin(np.array([geom.x for geom in ldn_points]),
    np.array([geom.y for geom in ldn_points]),
    gridsize=(70, int(70*h/w)),
    bins='log',
    mincnt=1,
    edgecolor='none',
    alpha=.9,
    cmap=plt.get_cmap('Blues'),
    ax=ax)

df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(
    x, fc='none', ec='#FFFF99', lw=1, alpha=1, zorder=1))
ax.add_collection(PatchCollection(df_map['patches'].values, match_original=True))

# copyright and source data info
smallprint = ax.text(
    1.08, 0.02,
    "Google Latitude data from 2010-2014\nProduced by Tyler Hartley\nInspired by sensitivecities.com",
    ha='right', va='bottom', size=figwidth/1.75,
    color='#555555', transform=ax.transAxes)

# Draw a map scale
m.drawmapscale(
    coords[0] + 0.05, coords[1] - 0.01,
    coords[0], coords[1],
    4., units='mi',
    barstyle='fancy', labelstyle='simple',
    fillcolor1='w', fillcolor2='#555555', fontcolor='#555555',
    zorder=5,
    ax=ax)

plt.title("Latitude Location History - Since 7/20/13",
          fontdict={'fontsize':20})
plt.tight_layout()

plt.savefig('data/location_history_7_20_13.png', dpi=300, frameon=False, transparent=True)

helpers.toc()

# <codecell>

"""<img id="zoom_01" src="small/image1.png" data-zoom-image="large/image1.jpg"/>"""
"""$("#zoom_01").elevateZoom();"""

# <headingcell level=1>

# Scratch

# <codecell>

# Plot all neighborhoods
for nhood in m.seattle:
    plt.plot([xx[0] for xx in nhood], [xx[1] for xx in nhood], 'b')
plt.plot(ld['latitudeE7'], ld['longitudeE7'])
plt.axis('scaled')

# <codecell>


out = ld.timediff[ld.timediff > -500]
out.hist(bins=100, figsize=(16,8))

# <codecell>

def sec_since_midnight(datetime_obj):
    return (datetime_obj.second + datetime_obj.minute*60 + 
                datetime_obj.hour*3600)
    

# <codecell>

times = ld.datetime.map(lambda x: sec_since_midnight(x))
times.hist(bins=24)

# <codecell>

# it can basically be assumed that, since July 20th, my phone has uploaded my location once a minute. 
# Slighly less at night than during the day (about 25% more frequenly durring waking hours)

