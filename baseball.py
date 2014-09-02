# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# <codecell>

# Some payroll data from http://www.baseballchronology.com/Baseball/Years/1977
xl_file = pd.ExcelFile(r'C:\Users\Tyler\Google Drive\DOCUMENTS\Blog Data\BaseballStats.xlsx')
salaries = xl_file.parse(sheetname='Salaries')
allstats = xl_file.parse(sheetname='Statistics')

allstats.Team = allstats.Team.map(lambda x: x.replace(u'\xa0', u" ")) #ascii issue; thanks, excel

allstats = pd.merge(allstats, salaries, how='left')
# let's play with a subset of data anyways
stats = allstats.reindex(columns=['Team', 'Year', 'W', 'Salary', 'Playoffs'])
stats.columns = [c.lower() for c in stats.columns]
del salaries # clear up some mem
del allstats # clear up some mem

# <codecell>

# Clean up salary data because, again, Excel is the worst.
def to_float(x):
    try:
        return float(x)    
    except:
        return float(x.replace(',','').strip())
    
stats.salary = stats.salary.map(to_float)

# <codecell>

# Let's just look at years where we have salary info
stats = stats[stats.year > 1976].reset_index(drop=True)

# <codecell>

# Normalize salary to fraction of total money spent that year
def add_prop(group):
    group['frac_salary'] = group.salary/group.salary.sum()*100
    return group
stats = stats.groupby('year').apply(add_prop)

# <codecell>

# Fix the weird MLB name issues
def team_groups(name):
    # Edge cases - 
    # 1. Anaheim/LA/Etc Angels
    # 2. Devil Rays vs Rays
    # 3. Miami/Florida Marlins
    if 'Angels' in name:
        return 'Los Angeles Angels'
    elif 'Tampa Bay' in name:
        return 'Tampa Bay Rays'
    elif 'Marlins' in name:
        return 'Miami Marlins'
    else:
        return name

stats.team = stats.team.map(team_groups)

# <codecell>

byteam = stats.groupby(by='team')
for i, g in byteam:
    color = 'b'
    zorder = None
    alpha = 0.5
    if 'Yankees' in i:
        color = 'k'
        zorder = 0
        alpha = 1
    if 'Red Sox' in i:
        color = 'r'
        zorder = 1
        alpha = 1
    
    plt.plot(g.year, g.frac_salary, color=color, alpha=alpha, linewidth=3, zorder=zorder)

# <codecell>

plt.plot?

# <codecell>


