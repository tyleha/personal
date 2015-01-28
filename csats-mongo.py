# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# ##By the Numbers
# * Number of total assignments completed
# * Average time spend answering all questions
# * Number of dropoffs at each stage -
#   * Dropoffs before submitting survey default form
#   * Dropoffs before submitting thank-you
# * HITs returned
# * Number of users who provided email contact
# * Tag cloud from a couple key questions
# 
# 
# Total Unique Visitors --	105
# 
# Completed Default Surveys --	59
# 
# Completed ThankYou Surveys --	49
# 
# Dropoffs During Default --	46
# 
# Dropoffs During ThankYou --	10
# 
# ##Takeaways
# 
# 
# 
# ##Random bits of info
# 
# * One user who has done 45 hits for us before forgot to click on 'Thank You' page and receive their completion code, but submitted a blank code anyways. Meh.
# * Many of the 10 who completed the Default survey but not the ThankYou survey simply waited too long to begin (xvZshFLgSAofKNrHc is a good example). In other words, they hoarded. They accepted the assignment, didn't fill in any questions for 11 of 15 minutes, then took longer than the remaining 4 to answer the default questions. Our app has no concept of time limits, so they were able to continue but then were unable to input our code into Turk (as that page would have timed out). Add timer to App moving forward? Would require some kind of Turk API query.
# * 66 users with assignments labeled "Complete", but only 49 people who completed the ThankYou survey. HOW?

# <codecell>

from pymongo import MongoClient
import pprint
from collections import OrderedDict

pp = pprint.PrettyPrinter(indent=4).pprint

client = MongoClient()
db = client.test01

# <codecell>

studyId = 'FKZsvL9sWpm8qNnZm'

surveyId = db.surveys.find_one({'studyId':studyId, 'purpose':'Default'})['_id']
surveyId_thankyou = db.surveys.find_one({'studyId':studyId, 'purpose':'ThankYou'})['_id']

assignments = list(db.assignments.find({'studyId':studyId}))

responses = list(db.responses.find({'surveyId':surveyId}))
responses_complete = list(db.responses.find({'surveyId':surveyId, 'isComplete':True}))
responses_incomplete = list(db.responses.find({'surveyId':surveyId, 'isComplete':{'$exists':False}}))
responses_thankyou = list(db.responses.find({'surveyId':surveyId_thankyou, 'isComplete':True}))

# <codecell>

len(list(db.responses.find({'surveyId':surveyId, 'isComplete':{'$exists':True}})))

# <codecell>

# General Stats
stats = OrderedDict()

stats['Total Unique Visitors'] = len(responses)
stats['Completed Default Surveys'] = len(responses_complete)
stats['Completed ThankYou Surveys'] = len(responses_thankyou)
stats['Dropoffs During Default'] = len(responses) - len(responses_complete)
stats['Dropoffs During ThankYou'] = len(responses_complete) - len(responses_thankyou)

for k, v in stats.iteritems():
    print k, '--\t', v

# <codecell>

# Write out to csv
import csv 

survey = db.surveys.find_one({'_id': surveyId})
question_names = [db.questions.find_one(questionId)['title'] for questionId in survey['questions']]
question_ids = [db.questions.find_one(questionId)['_id'] for questionId in survey['questions']]

with open('/home/tyleha/Study_Data_%s.csv'%studyId, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    keys = ['_id', 'userId', 'updatedAt', 'isComplete']
    
    # Write headers
    spamwriter.writerow(keys + ['isWholeHitComplete'] + question_names )
    for response in responses_complete:
        s = []
        for key in keys: 
            s.append(response[key])
            
        # Check for finishing whole HIT (if you did thankyou)
        s.append(db.responses.find_one({'userId': response['userId'], 'surveyId':surveyId_thankyou}) != None)
                 
        for qId in question_ids:
            try:
                s.append(response['answers'][qId]['comment'])
            except KeyError:
                # No answer for this question
                s.append('')
            
        spamwriter.writerow(s)
    

# <codecell>

# Create Word Clouds of answers
for idx, qId in enumerate(question_ids):
    text = ''
    for response in responses_complete:
        try:
            text += response['answers'][qId]['comment'] + ' '
        except:
            pass

    from wordcloud import WordCloud
    wordcloud = WordCloud(width=1000, height=600, max_words=50, max_font_size=500).generate(text)
    wordcloud.to_file('Wordcloud_%s.png'%question_names[idx])

# <codecell>

# Plots:
import matplotlib.pyplot as plt


# Plot of completions vs time 
# Great opportunity for map/reduce, next time
complete_dates = [db.assignments.find_one({'_id':response['assignmentId']})['createdAt'] for response in responses_complete]
complete_dates = sorted(complete_dates)

fig, ax = plt.subplots(figsize=(8,6))
ax.plot_date(complete_dates, range(len(complete_dates)), 'b-')
# Dropoffs
incomplete_dates = [db.assignments.find_one({'_id':response['assignmentId']})['createdAt'] for response in responses_incomplete]
incomplete_dates = sorted(incomplete_dates)
ax.plot_date(incomplete_dates, range(len(incomplete_dates)), 'r-')

ax.legend(['Completed', 'Dropoffs'], loc='lower right')
ax.set_title('Assignments over Time')
ax.set_ylabel('# Assignments')
ax.set_xlabel('Time')

# fig.autofmt_xdate()
import matplotlib.dates as dates
ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
fig.autofmt_xdate()




# <codecell>

# Why are there more assignments marked isComplete than there are ThankYou surveys?

# xx = db.assignments.find({'studyId':studyId, 'isComplete':True})
xx = db.assignments.find({'studyId':studyId, 'isComplete':False})
# for x in xx:
#     print db.responses.find_one({'assignmentId':x['_id'], 'surveyId': surveyId})
#     print x
#     print

# <codecell>


