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
    # Convert latitude and longitude to spherical coordinates in radians.
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

# <headingcell level=4>

# Load Latitude data

# <codecell>

with open('LocationHistory.json') as fh:
    raw = json.loads(fh.read())

ld = pd.DataFrame(raw['locations'])
del raw #free up some memory
ld.rename(columns={'latitudeE7':'latitude', 'longitudeE7':'longitude', 'timestampMs':'timestamp'}, inplace=True)
# convert to typical units
ld['latitude'] = ld['latitude']/float(1e7) 
ld['longitude'] = ld['longitude']/float(1e7)
ld['timestamp'] = ld['timestamp'].map(lambda x: float(x)/1000)
ld['datetime'] = ld.timestamp.map(datetime.datetime.fromtimestamp)
ld = ld[ld.accuracy < 1000] #Ignore locations with location estimates over 1000m
ld.reset_index(drop=True, inplace=True)

# <headingcell level=4>

# Import Seattle Shapefile data and start making Polygons

# <codecell>

shapefilename = r'data\Neighborhoods\WGS84\Neighborhoods'

shp = fiona.open(shapefilename+'.shp')
coords = shp.bounds
shp.close()

w, h = coords[2] - coords[0], coords[3] - coords[1]
extra = 0.01

# <codecell>

m = Basemap(
    projection='tmerc',
    lon_0=np.mean([coords[0], coords[2]]),
    lat_0=np.mean([coords[1], coords[3]]),
    ellps = 'WGS84',
    llcrnrlon=coords[0] - extra * w,
    llcrnrlat=coords[1] - (extra * h), 
    urcrnrlon=coords[2] + extra * w,
    urcrnrlat=coords[3] + (extra * h),
    resolution='i',
    suppress_ticks=True)
# Import the shapefile data to the Basemap 
out = m.readshapefile(shapefilename, name='seattle', drawbounds=False, color='none', zorder=2)

# <codecell>

# set up a map dataframe
df_map = pd.DataFrame({
    'poly': [Polygon(hood_points) for hood_points in m.seattle],
    'name': [hood['S_HOOD'] for hood in m.seattle_info]
})

# Create Point objects in map coordinates from dataframe lon and lat values
ld['distfromhome'] = distance_on_unit_sphere(ld.latitude, ld.longitude, 47.663794, -122.335812)*6367.1
ld['distfromwork'] = distance_on_unit_sphere(ld.latitude, ld.longitude, 47.639906, -122.378381)*6367.1
#Remove locations near work and home
ld = ld[(ld.distfromhome > 0.5) & (ld.distfromwork > 0.5)].reset_index(drop=True)

# Convert our latitude and longitude into Basemap cartesian map coordinates
mapped_points = [Point(m(mapped_x, mapped_y)) for mapped_x, mapped_y in zip(ld['longitude'], ld['latitude'])]
all_points = MultiPoint(mapped_points)
# Prep essentially optimizes the polygons for faster computation
hood_polygons = prep(MultiPolygon(list(df_map['poly'].values)))
# Filter out the points that do not fall within the map we're making
# and simultaneously count how many points fall within each polygon
city_points = filter(hood_polygons.contains, all_points)

# <headingcell level=2>

# Neighborhood Chloropleth Graph

# <codecell>

# Compute the points that belong in each neighborhood
from helpers import tic, toc
import copy
tic()

test_city_points = copy.copy(city_points)
hood_count = np.zeros(len(df_map))

idxs = range(len(df_map))
idxs.insert(0, idxs.pop(df_map[df_map.name.str.contains('Interbay')].index[0]))
idxs.insert(0, idxs.pop(idxs.index(df_map[df_map.name.str.contains('Wallingford')].index[0])))

for idx in idxs:
    pts = filter(prep(df_map.ix[idx].poly).contains, test_city_points)
    test_city_points = list(set(test_city_points)-set(pts))
    hood_count[idx] = len(pts)
    
df_map['hood_count'] = hood_count
toc()

# The code that actually needs to go into the blog:
# def num_of_contained_points(apolygon, city_points):
#     return int(len(filter(prep(apolygon).contains, city_points)))
    
# df_map['hood_count'] = df_map['poly'].apply(num_of_contained_points, args=(city_points,))

# <codecell>


df_map['hood_perc'] = df_map.hood_count/df_map.hood_count.sum()
df_map['hood_hours'] = df_map.hood_count/60.

# <codecell>

from pysal.esda.mapclassify import Natural_Breaks
from matplotlib.colors import Normalize as norm

# <codecell>

# Calculate Jenks natural breaks for density
breaks = Natural_Breaks(df_map[df_map['hood_hours'] > 0].hood_hours, initial=300, k=3)
df_map['jenks_bins'] = -1 #default value if no data exists for this bin
df_map['jenks_bins'][df_map.hood_count > 0] = breaks.yb

jenks_labels = ['Never been here', "> 0 hours"]+["> %d hours"%(perc) for perc in breaks.bins[:-1]]
print jenks_labels

# <codecell>

# Define your own breaks
breaks = [0., 4., 24., 64., 135., 1e12]
def self_categorize(entry, breaks):
    for i in range(len(breaks)-1):
        if entry > breaks[i] and entry <= breaks[i+1]:
            return i
    return -1
df_map['jenks_bins'] = df_map.hood_hours.apply(self_categorize, args=(breaks,))

jenks_labels = ['Never been\nhere']+["> %d hours"%(perc) for perc in breaks[:-1]]
print jenks_labels

# <codecell>

def custom_colorbar(cmap, ncolors, labels, **kwargs):    
    """Create a custom, discretized colorbar with correctly formatted/aligned labels.
    
    cmap: the matplotlib colormap object you plan on using for your graph
    ncolors: (int) the number of discrete colors available
    labels: the list of labels for the colorbar. Should be the same length as ncolors.
    """
    from matplotlib.colors import BoundaryNorm
    from matplotlib.cm import ScalarMappable
        
    norm = BoundaryNorm(range(0, ncolors), cmap.N)
    mappable = ScalarMappable(cmap=cmap, norm=norm)
    mappable.set_array([])
    mappable.set_clim(-0.5, ncolors+0.5)
    colorbar = plt.colorbar(mappable, **kwargs)
    colorbar.set_ticks(np.linspace(0, ncolors, ncolors+1)+0.5)
    colorbar.set_ticklabels(range(0, ncolors))
    colorbar.set_ticklabels(labels)
    return colorbar
    

# <codecell>

figwidth = 14
fig = plt.figure(figsize=(figwidth, figwidth*h/w))
ax = fig.add_subplot(111, axisbg='w', frame_on=False)

cmap = plt.get_cmap('Blues')
# draw neighborhoods with grey outlines
df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(x, ec='#111111', lw=.8, alpha=1., zorder=4))
pc = PatchCollection(df_map['patches'], match_original=True)
# apply our custom color values onto the patch collection
cmap_list = [cmap(val) for val in (df_map.jenks_bins.values - df_map.jenks_bins.values.min())/(
                  df_map.jenks_bins.values.max()-float(df_map.jenks_bins.values.min()))]
pc.set_facecolor(cmap_list)
ax.add_collection(pc)

#Draw a map scale
m.drawmapscale(coords[0] + 0.08, coords[1] + -0.01,
    coords[0], coords[1], 10.,
    fontsize=16, barstyle='fancy', labelstyle='simple',
    fillcolor1='w', fillcolor2='#555555', fontcolor='#555555',
    zorder=5, ax=ax,)

# ncolors+1 because we're using a "zero-th" color
cbar = custom_colorbar(cmap, ncolors=len(jenks_labels)+1, labels=jenks_labels, shrink=0.5)
cbar.ax.tick_params(labelsize=16)

fig.suptitle("    Time Spent in Seattle Neighborhoods", fontdict={'size':24, 'fontweight':'bold'}, y=0.92)
ax.set_title("  Using location data collected from my Android phone via Google Takeout", fontsize=14, y=0.98)
ax.text(1.35, 0.04, "Collected from 2012-2014 on Android 4.2-4.4\nGeographic data provided by data.seattle.gov", 
        ha='right', color='#555555', style='italic', transform=ax.transAxes)
ax.text(1.35, 0.01, "BeneathData.com", color='#555555', fontsize=16, ha='right', transform=ax.transAxes)
plt.savefig('chloropleth.png', dpi=300, frameon=False, transparent=False, bbox_inches='tight', pad_inches=0.5)

# <headingcell level=2>

# Hexbin Plot

# <codecell>

"""PLOT A HEXBIN MAP OF LOCATION
"""
figwidth = 14
fig = plt.figure(figsize=(figwidth, figwidth*h/w))
ax = fig.add_subplot(111, axisbg='w', frame_on=False)

# draw neighborhood patches from polygons
df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(
    x, fc='#555555', ec='#555555', lw=1, alpha=1, zorder=0))
# plot neighborhoods by adding the PatchCollection to the axes instance
ax.add_collection(PatchCollection(df_map['patches'].values, match_original=True))

# the mincnt argument only shows cells with a value >= 1
# The number of hexbins you want in the x-direction
numhexbins = 50
hx = m.hexbin(
    np.array([geom.x for geom in city_points]),
    np.array([geom.y for geom in city_points]),
    gridsize=(numhexbins, int(numhexbins*h/w)), #critical to get regular hexagon, must stretch to map dimensions
    bins='log', mincnt=1, edgecolor='none', alpha=1.,
    cmap=plt.get_cmap('Blues'))

# Draw the patches again, but this time just their borders (to achieve borders over the hexbins)
df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(
    x, fc='none', ec='#FFFF99', lw=1, alpha=1, zorder=1))
ax.add_collection(PatchCollection(df_map['patches'].values, match_original=True))

# Draw a map scale
m.drawmapscale(coords[0] + 0.05, coords[1] - 0.01,
    coords[0], coords[1], 4.,
    units='mi', barstyle='fancy', labelstyle='simple',
    fillcolor1='w', fillcolor2='#555555', fontcolor='#555555',
    zorder=5)

fig.suptitle("My location density in Seattle", fontdict={'size':24, 'fontweight':'bold'}, y=0.92)
ax.set_title("Using location data collected from my Android phone via Google Takeout", fontsize=14, y=0.98)
ax.text(1.0, 0.03, "Collected from 2012-2014 on Android 4.2-4.4\nGeographic data provided by data.seattle.gov", 
        ha='right', color='#555555', style='italic', transform=ax.transAxes)
ax.text(1.0, 0.01, "BeneathData.com", color='#555555', fontsize=16, ha='right', transform=ax.transAxes)
plt.savefig('hexbin.png', dpi=100, frameon=False, transparent=False, bbox_inches='tight', pad_inches=0.5)

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

ld['speed'] = ld.distance/(ld.timestamp - ld.timestamp.shift(-1))*3600 #km/hr

# Make a new dataframe containing the difference in location between each pair of points. 
# Any one of these pairs is a potential flight
flightdata = pd.DataFrame(data={'endlat':ld.latitude,
                             'endlon':ld.longitude,
                             'enddatetime':ld.datetime,
                             'distance':ld.distance,
                             'speed':ld.speed,
                             'startlat':ld.shift(-1).latitude,
                             'startlon':ld.shift(-1).longitude,
                             'startdatetime':ld.shift(-1).datetime,
                             }
                       ).reset_index(drop=True)

# <codecell>

# Weed out the obviously not-flights using very conservative criteria
flights = flightdata[(flightdata.speed > 40) & (flightdata.distance > 80)].reset_index()

#### Combine instances of flight that are directly adjacent 
# Find the indices of flights that are directly adjacent
_f = flights[flights['index'].diff() == 1]
adjacent_flight_groups = np.split(_f, (_f['index'].diff() > 1).nonzero()[0])

# Now iterate through the groups of adjacent flights and merge their data into
# one flight entry
for flight_group in adjacent_flight_groups:
    idx = flight_group.index[0] - 1 #the index of flight termination
    flights.ix[idx, ['startlat', 'startlon', 'startdatetime']] = [flight_group.iloc[-1].startlat, 
                                                         flight_group.iloc[-1].startlon, 
                                                         flight_group.iloc[-1].startdatetime]
    # Recompute total distance of flight
    flights.ix[idx, 'distance'] = distance_on_unit_sphere(flights.ix[idx].startlat,
                                                           flights.ix[idx].startlon,
                                                           flights.ix[idx].endlat,
                                                           flights.ix[idx].endlon)*6378.1   
    
# Cool. We're done! Now remove the "flight" entries we don't need anymore.
flights = flights.drop(f.index).reset_index(drop=True)

# Finally, we can be confident that we've removed instances of flights broken up by
# GPS data points during flight. We can now be more liberal in our constraints for what
# constitutes flight. I personally don't ever take flights shorter than a couple hundred miles,
# so let's remove any instances below 200km as a final measure.
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


