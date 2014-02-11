# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

class Point(object):
    '''it's a point in 2-D, dummy'''
    
class Rectangle(object):
    '''represents a rectangle 
       attributes: width, height, corner '''
    
import copy

def print_point(p):
    print '(%g, %g)' %(p.x, p.y)
    
def distance(p):
    return math.sqrt(p.x**2+p.y**2)

def find_center(box):
    p = Point()
    p.x = box.corner.x + box.width/2.0
    p.y = box.corner.y + box.height/2.0
    return p

def move_rectangle(box, dx, dy):
    newbox = copy.deepcopy(box)
    newbox.corner.x += dx
    newbox.corner.y += dy
    return newbox

def draw_rectangle(canvas, rec):
    
    bbox = [[box.corner.x,box.corner.y], [box.corner.x+box.width, box.corner.y+box.height]]
    canvas.rectangle(bbox, outline='black', width=2, fill=box.color)
    #canvas.circle([-25,0], 70, outline=None, fill='red')
    world.mainloop()
    
def draw_point(canvas, point):
    canvas.circle([point.x,point.y], 3, outline=None, fill='green')
    world.mainloop()

# <codecell>

import sys
sys.path.append('C:\Python27\Lib\site-packages\swampy-2.1.1-py2.7.egg\swampy')
from World import World

# <codecell>

box = Rectangle()
box.width = 100.0
box.height = 200.0
box.corner = Point()
box.corner.x = 0.0
box.corner.y = 0.0
box.color = 'red'

# <codecell>

world = World()
canvas = world.ca(width=500, height=500, background='white')
#draw_rectangle(canvas, box)
point = Point()
point.x = 30
point.y = 20
draw_point(canvas, point)

# <codecell>


