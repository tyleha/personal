# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

import helpers

# <codecell>


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

total_births = names.pivot_table(values='births', columns=['sex'], index=['year'], aggfunc=np.sum)

# <codecell>

total_births.plot()

# <codecell>


