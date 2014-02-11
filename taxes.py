# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import matplotlib.pyplot as plt
import numpy as np

# <codecell>

single = {2013: [(0.0, 0),
    (0.1, 8295),
    (0.15, 36250),
    (0.25, 87850),
    (0.28, 183250),
    (0.33, 398350),
    (0.35, 400000),
    (0.396, 1000000000),
    ],
    2014: [(0.0, 0),
    (0.1, 9075),
    (0.15, 36900),
    (0.25, 89350),
    (0.28, 186350),
    (0.33, 405100),
    (0.35, 406750),
    (0.396, 1000000000),
    ]
    }
standard_deduction = {2013:6100, 2014:6200}
personal_ex = {2013:3900, 2014:3950}

married = {2013: [(0.0, 0),
    (0.1, 17850), 
    (0.15, 72500), 
    (0.25, 146400), 
    (0.28, 223050), 
    (0.33, 398350),
    (0.35, 400000),
    (0.396, 1000000000),
    ],
    2014:[(0.0, 0),
    (0.1, 18150), 
    (0.15, 73800), 
    (0.25, 148850), 
    (0.28, 226850), 
    (0.33, 405100),
    (0.35, 457600),
    (0.396, 1000000000),
    ]
}

def marginal_tax(income, cutoffs):
    taxes = 0
    rmd = income
    for i in range(1, len(cutoffs)):
        rate, cutoff = cutoffs[i]
        prev_cutoff = cutoffs[i-1][1]
        if rmd <= cutoff-prev_cutoff:
            taxes += rmd*rate
            break
            
        taxes += (cutoff - prev_cutoff)*rate
        rmd = rmd - (cutoff - prev_cutoff)

    return taxes 

def income_tax(income, joint=False, deduction=None, year=2014):
    
    if deduction is None and joint is False:
        deduction = standard_deduction[year] + personal_ex[year]
    elif deduction is None and joint is True:
        deduction = (standard_deduction[year] + personal_ex[year])*2
    
    if joint:
        tax = marginal_tax(income-deduction, married[year])
    else:
        tax = marginal_tax(income-deduction, single[year])
    
    return tax

def income_and_fica(income, joint=False, deduction=None, year=2014):
    tax = income_tax(income, joint, deduction, year)
    tax += 0.0765*income
    return tax

# <codecell>

inc = 82500+4000+16000
print inc
print 'total tax is', income_tax(inc, joint=True)
print 'effective rate is', income_tax(inc, joint=True)/inc

# <codecell>

income_tax(16000, joint=False)

# <codecell>

efr = income_tax(inc, joint=True)/inc

# <codecell>

efr*3437.5-394

# <codecell>

x = np.array(range(10, 100))*1000
sdata = np.array([income_tax(inc, False)*2 for inc in x])
mdata = np.array([income_tax(inc, True) for inc in x])

# person a: 50k/year, single
# couple a: 50k/year each, single
# couble b: 50k/year each, married
plt.plot(x*2, sdata, 'b')
plt.plot(x, mdata, 'r')

# <codecell>

# Compare savings for different types of unmarried vs married couples
import matplotlib.cm as cm

incomes = np.array(range(0, 100, 2))*1000 
grid = np.zeros([len(incomes)]*2)
for i in range(len(incomes)):
    for j in range(len(incomes)):
        inci, incj = incomes[i], incomes[j]
        taxi = income_tax(inci, False)
        taxj = income_tax(incj, False)
        taxtot = income_tax(inci+incj, True)
        #raw dollar sum 
        grid[len(incomes)-i-1,j] = taxtot - taxi - taxj
        #grid[len(incomes)-i-1,j] = ((taxi+taxj)/(inci + incj) - taxtot/(inci+incj))*100


extent = [incomes[0], incomes[-1], incomes[0], incomes[-1]]
fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(111)
cmap_range = np.max([np.nanmax(grid), np.abs(np.nanmin(grid))])
col = ax.imshow(grid, extent=extent, cmap=cm.seismic, interpolation='none', vmin=-cmap_range, vmax=cmap_range)
fig.colorbar(col)

# <codecell>

np.min(grid)

# <codecell>

inc = 108500
tax = income_tax(inc, joint=True)
print tax/inc*82500/24

# <codecell>

print tax/inc

# <codecell>

income_tax(82500, joint=True)/82500.

# <codecell>

(442.993951613-394)*2

# <codecell>

5152-98

# <codecell>


