# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

d4.keys()

# <codecell>


# <codecell>

fin = open('C:\\Python27\\crosswd.txt')
       

def cartalk(fin):
    for line in fin:
        if len(line.strip())>5:

            for i in range(len(line.strip())-5):
                if line[i]==line[i+1] and line[i+2]==line[i+3] and line[i+4]==line[i+5]:
                    print line
                else: i += 1
        
cartalk(fin)            


# <codecell>

line = 'bannana'
'\.*nn' in line

# <headingcell level=1>

# Week 4

# <codecell>

def area(radius):
    temp = math.pi * radius**2
    temp = 8*xyz
    return temp

# <codecell>

def ackerman(m,n):
    if m == 0:
        return n+1
    elif m>0 and n==0:
        return ackerman(m-1,1)
    elif m>0 and n>0:
        return ackerman(m-1,ackerman(m, n-1))
        
print ackerman(3,4)
    
    



# <codecell>

def first(word):
    return word[0]

def last(word):
    return word[-1]

def middle(word):
    return word[1:-1]

# <codecell>

def is_palindrome(s):
    if first(s) == last(s) and len(s)>2:
        return is_palindrome(middle(s))
    elif first(s) == last(s) and len(s)==2:
        return True
    elif len(s) == 1:
        return True
    else:
        return False
    
print is_palindrome('bbb')
        

# <codecell>

def say(s):
    print s


def do_n(fun,s, n):
    if n <= 0:
        return n
    else:
        fun(s)
        do_n(fun,s,n-1)

do_n(say,'hey',6)

# <codecell>

p1, = plot([1,2,3])
p2, = plot([3,2,1])
p3, = plot([2,3,1])
legend((p2, p1), ("line 2", "line 1","line3"))

# <codecell>

' '*8

# <codecell>

c

