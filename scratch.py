# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
import numpy as np
import json

# <codecell>

xxx = """
Int64 hash (String s) {
        Int64 h = 7
        String letters = "acdegilmnoprstuw"
        for(Int32 i = 0; i < s.length; i++) {
            h = (h * 37 + letters.indexOf(s[i]))
        }
        return h
    }
"""

# <codecell>

Find a 9 letter string of characters that contains only letters from

acdegilmnoprstuw

such that the hash(the_string) is

945924806726376

ex: leepadg = 680131659347

# <codecell>

def myhash(astr):
    h = 7
    the_chars = 'acdegilmnoprstuw'
    for letter in astr:
        h = (h*37 + the_chars.index(letter))
    return h

the_chars = 'acdegilmnoprstuw'
the_hash = 945924806726376

def reverse_hash(anum):
    the_word = ''
    possible_indices = range(len(the_chars))
    numloops = 0
    
    while anum != 7 and numloops < 100:
        numloops += 1
        for idx in possible_indices:
            #print idx
            hashbit = ((anum - idx)/37.0)
            if hashbit%1 == 0:
                print hashbit, the_chars[idx]
                anum = hashbit
                the_word += the_chars[idx]
                break
    
    return the_word[::-1]

def reverse_algo(number, an_index):
    return (int(number) - int(an_index))/37

    

# <codecell>

res = reverse_hash(the_hash)
print res

# <codecell>

myhash(res)

# <codecell>

# step 0: h is 7
# step 1: multiply h by 37
# step 2: add the index of the character
# step 3: repeat...

# <codecell>

945924806726376

# <codecell>

4.0%1 == 0

# <codecell>


