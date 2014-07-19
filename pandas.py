# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

import helpers

# <codecell>

fn = 'usagov_bitly_data2013-05-17-1368832207'
fpath = helpers.user_prefix()+'Downloads\\'+fn

# <codecell>

print fpath

# <codecell>

buf = open(fpath, 'rb')
data = [json.loads(line) for line in buf]

# <codecell>

frame = pd.DataFrame(data)

# <codecell>

cframe = frame[frame['a'].notnull()]

# <codecell>

['Android' in cf for cf in cframe['a'][:20]]
np.where(cframe['a'])

# <codecell>

np.where(cframe['a'].str.contains('Android'), 'Android', 'Other')

# <codecell>


