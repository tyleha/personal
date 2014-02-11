# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

class Point(object):
    """represents a point in 2-D space"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def __str__(self):
        return '(%d,%d)'%(self.x,self.y)
    
    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x+other.x,self.y+other.y)
        elif isinstance(other, tuple):
            return Point(self.x+other[0],self.y+other[1])
        
    def __radd__(self, other):
        return self.__add__(other)
            
    
    def distance(self):
        return math.sqrt(x**2+y**2)
    
    
   

# <codecell>

p1 = Point(3,3)
p2 = Point(1,2)
print (3,3) + p2

# <rawcell>

# his exercise is a cautionary tale about one of the most common, and difficult to find, errors in Python.
# 
# Write a definition for a class named Kangaroo with the following methods:
# An __init__ method that initializes an attribute named pouch_contents to an empty list.
# A method named put_in_pouch that takes an object of any type and adds it to pouch_contents.
# A __str__ method that returns a string representation of the Kangaroo object and the contents of the pouch.
# Test your code by creating two Kangaroo objects, assigning them to variables named kanga and roo, and then adding roo to the contents of kanga’s pouch.

# <codecell>

class Kangaroo(object):
    def __init__(self, pouch_contents=[]):
        self.pouch_contents = pouch_contents
        
    def put_in_pouch(self, obj):
        self.pouch_contents.append( obj)
        
    def __str__(self):
        return 'Contents are %s'%(self.pouch_contents)
        
kang = Kangaroo()
roo = Kangaroo()
        
kang.put_in_pouch(roo)
        

# <codecell>

print kang

# <codecell>


