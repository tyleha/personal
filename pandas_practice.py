# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Bitly Data

# <codecell>

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

import helpers

# <codecell>

fn = 'usagov_bitly_data2013-05-17-1368832207'
fpath = helpers.user_prefix()+'Downloads\\'+fn
print fpath

# <codecell>

buf = open(fpath, 'rb')
data = [json.loads(line) for line in buf]

# <codecell>

frame = pd.DataFrame(data)

# <codecell>

cframe = frame[frame['a'].notnull()]

# <codecell>

operating_system = np.where(cframe['a'].str.contains('Android'), 'Android', 'Other')

# <codecell>

operating_system.value_counts()

# <codecell>

by_tz_os = cframe.groupby(['tz', operating_system])

# <codecell>

res = by_tz_os.size().unstack(level=0).fillna(0)

# <codecell>

print res

# <headingcell level=1>

# Name Data

# <codecell>

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# <codecell>

years = range(1880, 2014)
bits = list()
folder = r'C:\Users\thartley\Downloads\names'

for year in years:
    fn = folder+'\\'+'yob%s.txt'%year
    frame = pd.read_csv(fn, names=['name', 'sex', 'births'])
    frame['year'] = int(year)
    
    bits.append(frame)
    
names = pd.concat(bits, ignore_index=True)
    

# <codecell>

def add_prop(group):
    births = group.births.astype(float)
    group['prop'] = births/births.sum()
    return group

names = names.groupby(['year', 'sex']).apply(add_prop)

# <codecell>

def sort_groups_by(group, keyword):
    return group.sort_index(by=keyword, ascending=False)

group = names.groupby(['year', 'sex']).apply(sort_groups_by, keyword='births')
boys = group[group.sex == 'M']
girls = group[group.sex == 'F']


# <codecell>

# Let's figure out the set of names that have ever held the #1 position
most_popular_boys = boys.groupby('year').first()
number_one_boys_names = set(most_popular_boys.name)

most_popular_girls = girls.groupby('year').first()
number_one_girls_names = set(most_popular_girls.name)

# <codecell>

_boys = boys.pivot_table(values='prop', columns='name', index='year', aggfunc=np.sum)
best_boys = _boys[list(number_one_boys_names)]
ax = best_boys.plot()
ax.set_ylabel('Fraction of total names')

# <codecell>

_girls = girls.pivot_table(values='prop', columns='name', index='year', aggfunc=np.sum)
best_girls = _girls[sorted(list(number_one_girls_names))]
ax = best_girls.plot()
ax.set_ylabel('Fraction of total names')

# <headingcell level=3>

# Scratch

# <codecell>

df = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar',
   ...:                        'foo', 'bar', 'foo', 'foo'],
   ...:                 'B' : ['one', 'one', 'two', 'three',
   ...:                        'two', 'two', 'one', 'three'],
   ...:                 'C' : 22, 'D' : 33})

# <codecell>

foo = df.groupby('A')

# <codecell>

df2 = pd.DataFrame({'X' : ['B', 'B', 'A', 'A'], 'Y' : [1, 2, 3, 4]})

# <codecell>

df2.groupby(['X']).count()

# <codecell>


