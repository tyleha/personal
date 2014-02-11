# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import csv

# <codecell>

data = {}

with open(r'C:\Users\Tyler\Desktop\rec_blank_counts_example.csv', 'r') as csvfile:
    somereader = csv.reader(csvfile)
    for i, row in enumerate(somereader):
        #Ugh, skip first line (header)
        if i == 0: continue

        linct = int(row[0]); subj = row[1].lower(); task = row[2].upper()
        
        #If we haven't seen this subject yet, init variables
        if subj not in data.keys():
            data[subj] = {}
            data[subj][task] = 0
         
        #But if this subject exists but we haven't seen this
        #task yet, init variable
        elif task not in data[subj].keys():
            data[subj][task] = 0
        
        #Ready to do the actual math: add if 0
        if linct == 0:
            data[subj][task] += 1

# <codecell>

#Open up a csv file
dest_filename = r'Subject_Report.csv'

with open(dest_filename, 'wb') as subjectfile:
    spamwriter = csv.writer(subjectfile, dialect='excel')
    spamwriter.writerow(['Subject','Task','Number of Linecounts eq to Zero'])
    
    #Actually write stuff to csv
    for subj, tasks in data.iteritems():
        for task, numzero in tasks.iteritems():
            spamwriter.writerow([subj, task, numzero])

# <codecell>

f = open('errors.txt', 'a')

# <codecell>

f.write('tyleha@gmail.com')

# <codecell>

f.close()

# <codecell>


