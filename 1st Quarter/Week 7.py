# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%load_ext autoreload
%autoreload 2
from computing_imports import *

def sort_by_length(words):
    t = []
    
    for word in words:
       t.append((len(word),  random.random(), word))

    t.sort(reverse=False)

    res = []
    for length, r, word in t:
        res.append(word)
    return res

# <codecell>

words = 'theres not much i would rather do than spend a day sailing high with you hey nay bad bot way rag'
words = words.split(' ')

sort = sort_by_length(words)

# <codecell>

import re

def most_frequent(text):
    
    freqs = dict()
    
    for letter in str.lower(text):
        if re.match('[a-zA-Z]',letter):
            freqs[letter] = freqs[letter]+1 if letter in freqs.keys() else 1
            
    tot = sum(freqs.values())
    for letter in freqs.keys():
        freqs[letter] = format(freqs[letter]/float(tot)*100,'.2f') 
        
    return freqs
    
    
f = open(os.getcwd()+'\\.ipython\\english.txt','r')
text = f.read()

freqs = most_frequent(text)

# <codecell>

f = open(os.getcwd()+'\\words.txt','r')
wordlist = f.read()
children('baskzet', wordlist)

# <codecell>

word = 'hello'
x = list(word[:])
xx = list(x
a = xx.remove('h')

# <headingcell level=4>

# Chpt 11

# <codecell>

f = open(os.getcwd()+'\\.ipython\\english.txt','r')
wordlist = f.readlines()
#wordlist = wordlist.split('\\')
                          

#wordlist[:400]
xx = wordlist[0].strip()
xx.replace('', '')

# <codecell>

def makewords(wordlist):
    xx = []
    for line in wordlist:
        
        line = line.replace('-', ' ')
        
        for word in line.split():
            word = word.strip(string.punctuation + string.whitespace)
            word = word.lower()
            xx.append(word)

    return xx

def markov(words):
    m = dict()
    
    for i in range(0,len(words)-2):
        prefix = tuple(words[i:i+2])
        suffix = words[i+2]
        
        if prefix in m and m[prefix] != None:
            m[prefix] = m[prefix].append(suffix)
        elif [suffix] != None:
            m[prefix] = [suffix]
    return m

# <codecell>


f = open(os.getcwd()+'\\.ipython\\english.txt','r')
wordlist = f.readlines()
words = makewords(wordlist)

m = markov(words)
x = words[9]
t = {tuple(words[7:9]) :[x]}

# <codecell>

for v in m.values():
    if len(v)>1:
        print v

# <codecell>

t[tuple(words[7:9])]

# <codecell>

%qtconsole

# <codecell>


