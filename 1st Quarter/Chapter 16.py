# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

class Time(object):
    """represents the time of day.
       attributes: hour, minute, second"""
    
    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return '%d:%.2d:%.2d' %(self.hour, self.minute, self.second)
        
    def in_seconds(self):
        return self.hour*3600+self.minute*60+self.second
        
    def __add__(self, other):
        return in_24hr_time(self.in_seconds()+other.in_seconds())

def valid_time(time):
    if time.hour < 0 or time.minute < 0 or time.second < 0:
        return False
    if time.minute >= 60 or time.second >= 60:
        return False
    return True

def in_24hr_time(seconds):
    time = Time()
    seconds = int(seconds)
    
    time.hour = seconds/3600
    time.minute = (seconds - time.hour*3600)/60
    time.second = (seconds - time.hour*3600 - time.minute*60)
    
    return time
    
def is_after(t1, t2):
    return in_seconds(t1) > in_seconds(t2)

def increment(time, seconds):
    assert valid_time(time)
    ts = in_seconds(time)
    ts += seconds
    return in_24hr_time(ts)

def add_time(t1,t2):
    assert valid_time(t1) and valid_time(t2)
    seconds = in_seconds(t1) + in_seconds(t2)
    return in_24hr_time(seconds)


def mul_time(t, m):
    return in_24hr_time(m*in_seconds(t))

def avg_pace(t, dist):
    return mul_time(t, 1/dist)


# <codecell>

t1 = Time()
t1.hour = 2
t1.minute = 3
t1.second = 0

t2 = Time()
t2.hour = 10
t2.minute = 59
t2.second = 0

# <codecell>

print t1+t2

# <codecell>

class Date(object):
    '''year, month, day'''
    def __init__(self, year = None, month = None, day = None):
        self.year = year
        self.month = month
        self.day = day
    
    def print_date(self):
        print '%d/%d/%d' %(self.month, self.day, self.year)
        
    days = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
    def increment(self, n):
        if self.year%4 == 0:
            days[2] = 29
        
        (days[self.month] - self.days)
        
        
d1 = Date(1987, 7, 13)
d1.print_date()

# <codecell>


