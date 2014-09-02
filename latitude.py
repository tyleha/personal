# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Google Latitude Analysis

# <markdowncell>

# ### To Do - make this a narrative fitting of a blog
# 1. ~~Plot the chloropleth of neighborhoods~~
# 2. Remove time at work and home from data and re-plot
# 3. ~~Find farthest point traveled~~
# 4. ~~Calculate number of flights taken~~
# 
#     

# <codecell>

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

def distance_on_unit_sphere(lat1, long1, lat2, long2):
    
    # http://www.johndcook.com/python_longitude_latitude.html
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = np.pi/180.0  
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
    
    cos = (np.sin(phi1)*np.sin(phi2)*np.cos(theta1 - theta2) + 
           np.cos(phi1)*np.cos(phi2))
    arc = np.arccos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc

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
    colors_i = np.concatenate((np.linspace(0, 1., N), (0., 0., 0., 0.)))
    colors_rgba = cmap(colors_i)
    indices = np.linspace(0, 1., N + 1)
    cdict = {}
    for ki, key in enumerate(('red', 'green', 'blue')):
        cdict[key] = [(indices[i], colors_rgba[i - 1, ki], colors_rgba[i, ki]) for i in xrange(N + 1)]
    return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d" % N, cdict, 1024)

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

ld = pd.DataFrame(raw['locations'])
ld.rename(columns={'latitudeE7':'latitude', 'longitudeE7':'longitude', 'timestampMs':'timestamp'}, inplace=True)
del raw
ld['latitude'] = ld['latitude']/float(1e7)
ld['longitude'] = ld['longitude']/float(1e7)
ld['timestamp'] = ld['timestamp'].map(lambda x: float(x)/1000)
ld['datetime'] = ld.timestamp.map(datetime.datetime.fromtimestamp)
ld = ld[ld.timestamp > 1374303600.0] #time since Jul. 20, 2013 when data reporting increased
ld = ld[ld.accuracy < 1000] #Ignore locations with location estimates over 1000m?
ld.reset_index(drop=True, inplace=True)

# <headingcell level=2>

# Import Seattle Shapefile data and start making Polygons

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

zzz ="""
m2 = Basemap(
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
out = m2.readshapefile(
    helpers.user_prefix() + r'data\Shorelines\WGS84\Shorelines',
    'water',
    color='none',
    zorder=2)
"""

# <codecell>

# set up a map dataframe
df_map = pd.DataFrame({
    'poly': [Polygon(xy) for xy in m.seattle],
    'name': [nhood['S_HOOD'] for nhood in m.seattle_info]})
df_map['area_m'] = df_map['poly'].map(lambda x: x.area)
df_map['area_km'] = df_map['area_m'] / 100000
#df_map['poly'].append(Polygon(m2.water[0]))

# <codecell>

# Create Point objects in map coordinates from dataframe lon and lat values
#ld['distfromhome'] = distance_on_unit_sphere(ld.latitude, ld.longitude, 47.663794, -122.335812)*6367.1
#ld['distfromwork'] = distance_on_unit_sphere(ld.latitude, ld.longitude, 47.639906, -122.378381)*6367.1
#ld = ld[(ld.distfromhome > 0.3) & (ld.distfromwork > 0.5)].reset_index(drop=True)

map_points = pd.Series([Point(m(mapped_x, mapped_y)) for mapped_x, mapped_y in zip(ld['longitude'], ld['latitude'])])

all_points = MultiPoint(list(map_points.values))
hood_polygons = prep(MultiPolygon(list(df_map['poly'].values)))

city_points = filter(hood_polygons.contains, all_points)

# <headingcell level=2>

# Neighborhood Chloropleth Graph

# <codecell>

# Compute the points that belong in each neighborhood
def num_of_contained_points(apolygon, city_points):
    return int(len(filter(prep(apolygon).contains, city_points)))
    
df_map['hood_count'] = df_map['poly'].apply(num_of_contained_points, args=(city_points,))
#df_map['hood_count'] = df_map['poly'].map(lambda x: int(len(filter(prep(x).contains, city_points))))b

# <codecell>

df_map['hood_perc'] = df_map.hood_count/df_map.hood_count.sum()
df_map['hood_hours'] = df_map.hood_count/60.

# <codecell>

from pysal.esda.mapclassify import Natural_Breaks
from matplotlib.colors import Normalize

# <codecell>

# Calculate Jenks natural breaks for density
breaks = Natural_Breaks(df_map[df_map['hood_hours'] > 0].hood_hours, initial=300, k=5)

jb = pd.DataFrame({'jenks_bins': breaks.yb}, index=df_map[df_map.hood_count > 0].index)
try:
    df_map = df_map.join(jb)
except:
    df_map.jenks_bins = jb
df_map.jenks_bins.fillna(-1, inplace=True)

jenks_labels = ["> %d hours"%(perc) for perc in breaks.bins[:-1]]
jenks_labels = ['Have never been here', "> 0 hours"]+jenks_labels
print jenks_labels

# <codecell>

breaks = [0., 4., 24., 64., 135., 1e12]
def self_categorize(entry, breaks):
    for i in range(len(breaks)-1):
        if entry > breaks[i] and entry <= breaks[i+1]:
            return i
    else:
        return -1
jb = df_map.hood_hours.apply(self_categorize, args=(breaks,))
try:
    df_map = df_map.join(jb)
except:
    df_map.jenks_bins = jb
jenks_labels = ["> %d hours"%(perc) for perc in breaks[:-1]]
jenks_labels = ['Have never been here']+jenks_labels
print jenks_labels

# <codecell>

plt.clf()
figwidth = 14
fig = plt.figure(figsize=(figwidth, figwidth*h/w))
ax = fig.add_subplot(111, axisbg='w', frame_on=False)

# use a blue colour ramp - we'll be converting it to a map using cmap()
cmap = plt.get_cmap('Blues')
# draw wards with grey outlines
df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(x, ec='#111111', lw=.8, alpha=1., zorder=4))
pc = PatchCollection(df_map['patches'], match_original=True)
# impose our colour map onto the patch collection
norm = Normalize()
pc.set_facecolor(cmap(norm(df_map['jenks_bins'].values)))
ax.add_collection(pc)

# Add a colour bar
cb = colorbar_index(ncolors=len(jenks_labels), cmap=cmap, shrink=0.5, labels=jenks_labels)
cb.ax.tick_params(labelsize=16)

"""
# Bin method, copyright and source data info
smallprint = ax.text(
    1.03, 0,
    'Classification method: natural breaks\nContains Ordnance Survey data\n$\copyright$ Crown copyright and database right 2013\nPlaque data from http://openplaques.org',
    ha='right', va='bottom',
    size=4,
    color='#555555',
    transform=ax.transAxes)
"""
# Draw a map scale
m.drawmapscale(
    coords[0] + 0.08, coords[1] + -0.002,
    coords[0], coords[1],
    10.,
    fontsize=16,
    barstyle='fancy', labelstyle='simple',
    fillcolor1='w', fillcolor2='#555555',
    fontcolor='#555555',
    zorder=5)

# this will set the image width to 722px at 100dpi
plt.title("Time Spent in Seattle Neighborhoods", fontsize=16)
plt.tight_layout()
plt.savefig('data/chloropleth.png', dpi=300, frameon=False, transparent=True)

# <headingcell level=2>

# Hexbin Plot

# <codecell>

"""PLOT A HEXBIN MAP OF LOCATION
"""

helpers.tic()

# draw ward patches from polygons
df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(
    x, fc='#555555', ec='#555555', lw=1, alpha=1, zorder=0))

plt.clf()
figwidth = 14
fig = plt.figure(figsize=(figwidth, figwidth*h/w))
ax = fig.add_subplot(111, axisbg='w', frame_on=False)

# plot boroughs by adding the PatchCollection to the axes instance
ax.add_collection(PatchCollection(df_map['patches'].values, match_original=True))

# the mincnt argument only shows cells with a value >= 1
# hexbin wants np arrays, not plain lists
hx = m.hexbin(
    np.array([geom.x for geom in city_points]),
    np.array([geom.y for geom in city_points]),
    gridsize=(70, int(70*h/w)),
    bins='log',
    mincnt=1,
    edgecolor='none',
    alpha=1.,
    cmap=plt.get_cmap('Blues'))

df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(
    x, fc='none', ec='#FFFF99', lw=1, alpha=1, zorder=1))
ax.add_collection(PatchCollection(df_map['patches'].values, match_original=True))

# copyright and source data info
smallprint = ax.text(
    1.08, 0.0,
    "Google Latitude data from 2010-2014\nProduced by Tyler Hartley\nInspired by sensitivecities.com",
    ha='right', va='bottom',
    size=figwidth/1.75,
    color='#555555',
    transform=ax.transAxes)

# Draw a map scale
m.drawmapscale(
    coords[0] + 0.05, coords[1] - 0.01,
    coords[0], coords[1],
    4.,
    units='mi',
    barstyle='fancy', labelstyle='simple',
    fillcolor1='w', fillcolor2='#555555',
    fontcolor='#555555',
    zorder=5)

plt.title("Latitude Location History - Since 7/20/13")
#plt.tight_layout()
# this will set the image width to 722px at 100dpi
#fig.set_size_inches(7., 10.5)
plt.savefig('data/hexbin.png', dpi=300, frameon=False, transparent=True)

helpers.toc()

plt.show()


# <headingcell level=1>

# Flights Taken

# <codecell>

degrees_to_radians = np.pi/180.0 
ld['phi'] = (90.0 - ld.latitude) * degrees_to_radians 
ld['theta'] = ld.longitude * degrees_to_radians

ld['distance'] = np.arccos( 
    np.sin(ld.phi)*np.sin(ld.phi.shift(-1)) * np.cos(ld.theta - ld.theta.shift(-1)) + 
    np.cos(ld.phi)*np.cos(ld.phi.shift(-1))
    ) * 6378.100 # radius of earth in km

ld['speed'] = ld.distance/(ld.timestamp - ld.timestamp.shift(-1))*3600

# Identify potential flights
travelindex = ld[(ld['speed'] > 10) & (ld['distance'] > 80.)].index
print "Found %s instances of flights"%len(travelindex)

# <codecell>

# Make DataFrame of Flights taken with new columns: beginlat, beginlon, endlat, endlon, 
# begin, end, distance, speed

flights = pd.DataFrame(data={'endlat':ld.ix[travelindex].latitude,
                             'endlon':ld.ix[travelindex].longitude,
                             'enddatetime':ld.ix[travelindex].datetime,
                             'distance':ld.ix[travelindex].distance,
                             'speed':ld.ix[travelindex].speed,
                             },
                       ).reset_index()
flights['startlat'] = ld.ix[travelindex+1].latitude.reset_index(drop=True)
flights['startlon'] = ld.ix[travelindex+1].longitude.reset_index(drop=True)
flights['startdatetime'] = ld.ix[travelindex+1].datetime.reset_index(drop=True)

# Clean up flights that have random GPS data in the middle of them
f = flights[flights['index'].diff() == 1]
cuts = np.split(f, (f['index'].diff() > 1).nonzero()[0])

for cut in cuts:
    flight_origin = cut.iloc[-1]
    idx = cut.index[0]-1
    flights.ix[idx, 'startlat'] = flight_origin.startlat
    flights.ix[idx, 'startlon'] = flight_origin.startlon
    flights.ix[idx, 'startdatetime'] = flight_origin.startdatetime
    flights.ix[idx, 'startlat'] = flight_origin.startlat
    flights.ix[idx, 'distance'] = distance_on_unit_sphere(flights.ix[idx].startlat,
                                                       flights.ix[idx].startlon,
                                                       flights.ix[idx].endlat,
                                                       flights.ix[idx].endlon)*6378.1

flights = flights.drop(f.index).reset_index(drop=True)
flights = flights[flights.distance > 200].reset_index(drop=True)

# <codecell>

fig = plt.figure(figsize=(18,12))

#fly = flights[(flights.startlon < 0) & (flights.endlon < 0)]# Western Hemisphere Flights
fly = flights[(flights.startlon > 0) & (flights.endlon > 0)] # Eastern Hemisphere Flights
#fly = flights # All flights. Need to use Robin projection w/ center as -180 as 2 cross 180/-180 Lon

buf = .3
minlat = np.min([fly.endlat.min(), fly.startlat.min()])
minlon = np.min([fly.endlon.min(), fly.startlon.min()])
maxlat = np.max([fly.endlat.max(), fly.startlat.max()])
maxlon = np.max([fly.endlon.max(), fly.startlon.max()])
width = maxlon - minlon
height = maxlat - minlat


m = Basemap(llcrnrlon=minlon - width*buf,
            llcrnrlat=minlat - height*buf*1.5,
            urcrnrlon=maxlon + width*buf,
            urcrnrlat=maxlat + height*buf,
            projection='merc', #'robin',
            resolution='l',
            #lat_1=minlat, lat_2=maxlat,
            lat_0=minlat + height/2,
            lon_0=minlon + width/2,)
            #lon_0=-180)

m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.fillcontinents()

#m.drawparallels(np.arange(pts.latitude.min(),pts.latitude.max(),2.), labels=[1,1,1,1], fmt="%0.1f")
#m.drawmeridians(np.arange(pts.longitude.min(), pts.longitude.max(),5.), labels=[1,1,1,1], fmt="%0.1f")

for f in fly.iterrows():
    f = f[1]
    m.drawgreatcircle(f.startlon, f.startlat, f.endlon, f.endlat, linewidth=3, alpha=0.4, color='b' )
    m.plot(*m(f.startlon, f.startlat), color='g', alpha=0.8, marker='o')
    m.plot(*m(f.endlon, f.endlat), color='r', alpha=0.5, marker='o' )
    #pa = Point(m(f.startlon, f.startlat))
    #pb = Point(m(f.endlon, f.endlat))
    #plt.plot([pa.x, pb.x], [pa.y, pb.y], linewidth=4)
plt.savefig('data/flightdata.png', dpi=300, frameon=False, transparent=True)

# <headingcell level=1>

# Scratch

# <codecell>

flights.distance.sum()

# <codecell>

ld.ix[253164-5:253164+5]

# <codecell>

flights.ix[26,'index']

# <codecell>


