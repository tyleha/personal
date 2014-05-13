# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
import numpy as np
import json

# <codecell>

fn = r'C:\Users\thartley\Desktop\usagov_bitly_data2013-05-17-1368817803'
records = [json.loads(line) for line in open(fn)]

# <codecell>

records[0]

# <codecell>

frame = pd.DataFrame(records)

# <codecell>

frame['tz'][:10].plot(kind='barh', rot=0)

# <codecell>

tzinfo = frame['tz'].value_counts()

# <codecell>

tzinfo[:10].plot(kind='barh', rot=0)

# <codecell>

x = np.arange(1.3e6, 8.0e6, 0.2e6)
y = np.arange(1.3e6, 8.0e6, 0.2e6)

# <codecell>

z1, z2 = np.meshgrid(x, y)

# <codecell>

refl = (z1-z2)**2/(z1+z2)**2

# <codecell>

plt.imshow(refl)

# <codecell>

fig = plt.figure()
ax = fig.add_subplot(111)
out = ax.hexbin(z1.ravel(), z2.ravel(), C=refl.ravel(), gridsize=20)
cb = fig.colorbar(out)
ax.set_title("Acoustic Impedance Reflection")
ax.set_ylabel("Impedance A")
ax.set_xlabel("Impedance B")
fig.tight_layout()
t = """Material z [kg/(m2s]
Fat     1.30e6
Water   1.50e6 
Muscle  1.65e6
Bone    7.80e6"""
ax.text(x[-12], y[-8], t, color='white')

# <codecell>



