# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd

# <codecell>

df = pd.DataFrame(np.random.rand(10, 10))

# <codecell>

df.resample(0.2)

# <codecell>

index = pd.date_range('1/1/2001 00:00:00', '1/1/2001 00:00:10', freq='10L')
s = pd.Series(np.random.randn(index.size), index=index)

# <codecell>

print len(s)
ns = s.resample('2.5S')
print len(ns)

# <codecell>

s.resample('5Min')

# <codecell>


