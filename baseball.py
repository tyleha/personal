# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Baseball salary analysis
# ## Flow
# 1. Increase in total league salary over time As compared to a variety of market metrics
# 2. Team salary graph over time. Point out notable teams. Compare both %spending and #rank
# 3. The big question - does money buy wins?
#     1. All year plot of wins (or win%) vs %spending. Draw conclusions
#     2. Plot of Slope of line from year to year with 95% CI error bars
#     3. dStd over time - has the spending of money become more or less diverse?
# 4. Assuming we see a minimal correlation between money and success, what is our hypothesis? Of late - 6 yr team ownership. Plot wins vs salary but color/size dots based on team avg age.

# <codecell>

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import wolframalpha as wa

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

# <headingcell level=1>

# 1. Total League Salary

# <codecell>

# Let's just look at years where we have salary info
stats = stats[stats.year > 1976].reset_index(drop=True)

# <codecell>

league_salary = stats.groupby('year').salary.sum()

# <codecell>

ff = pd.ExcelFile(r'C:\Users\thartley\Documents\Dropbox\prices.xlsx')
incomes = ff.parse('household')
incomes = incomes[incomes.year > 1976].reset_index(drop=True)
textbooks = ff.parse('textbooks')
textbooks = pd.DataFrame([textbooks.ix[i] for i in range(0, len(textbooks), 12)])
textbooks['year'] = textbooks.month.map(lambda x: x.year)
textbooks = textbooks[textbooks.year > 1976].reset_index(drop=True)

# <codecell>

plt.figure()
plt.plot(incomes.year, incomes.nominal)
plt.plot(textbooks.year, textbooks.CPI*(incomes.nominal.iloc[-1]/textbooks.CPI[0]))

# <codecell>

incomes.nominal.iloc[-1]

# <codecell>

"""
wolfram_api_id = "G3Y8VX-E83L2YWY59"
client = wa.Client(wolfram_api_id)

res = client.query('{0} {1} dollars in 2013 dollars'.format(1000, 1977))

for r in res.results:
    price =  float(re.findall('^\$([\d.]+)', r.text)[0])
    break
"""

# <codecell>

fig = plt.figure(figsize=(12,8))
plt.plot(league_salary.year, league_salary.salary)
plt.plot()

# <headingcell level=1>

# 2. Team Salary over Time

# <codecell>

# Normalize salary to fraction of total money spent that year
def add_prop(group):
    group['frac_salary'] = group.salary/group.salary.sum()*100
    return group
stats = stats.groupby('year').apply(add_prop)

# <codecell>

byteam = stats.groupby(by='team')
for i, g in byteam:
    color = 'k'
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


# <codecell>


