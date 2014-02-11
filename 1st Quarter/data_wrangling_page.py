# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# #Introduction
# 1. Clean data is pushed to the google cloud.  
#     1.  Collect log data from sources (local, S3)  
#     1.  Amalgamate log files into task    
#     1.  Push to cloud (Google)  

# <codecell>

#%load_ext autoreload
#%autoreload 2

from collections import defaultdict, OrderedDict
from itertools import groupby
import httplib2
import sys
import json
import pprint
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from apiclient.errors import HttpError
from fetch.flow import FLOW
from scipy import cluster
import numpy as np
import pandas as pd
#Global Vars
storage_location = 'bigquery_web.dat'

# <markdowncell>

# #Amalgamate Logs:

# <markdowncell>

# ##Normalize TimData

# <codecell>

#(rows,cols) = features.shape
        #normFeatures = np.zeros((rows,cols))

        #print rows, cols
        #for col in range(cols):
         #   feature = features[:,col]
        
            #Retrieve 2nd and 98th thresholds
            #lowNormT =  float(thresholds[sensors[col]]['lowNorm'])
            #highNormT = float(thresholds[sensors[col]]['highNorm'])
    
            #Perform normalization as based on Tim Code (i.e. Map 2nd and 98th perc. to [-1 1]
            #features[:,col] = (feature - lowNormT)* (2/(highNormT-lowNormT)) - 1
    
        #normFeatures now normalized version of features '''

# <codecell>

y = '''def normalize(task, col, thresholds):
    qsCol = "SELECT {0} FROM [data.{1}] WHERE task='{2}'".format(col, table_name, task)
    results = queryGoogle(qsCol)
    feature = (np.array([[float(field['v']) for field in row['f']]for row in results['rows']]))
    lowNormT = float(thresholds[task][col]['lowNorm'])
    highNormT = float(thresholds[task][col]['highNorm'])
    normal = (feature - lowNormT)* (2/(highNormT-lowNormT)) - 1
    return normal.tolist()
    
def normalizeTimData():
    table_name = 'timdata'
    import numpy as np
    tasks = ['cutting', 'suturing', 'pegtransfer']# ['cutting'] #
    columns = [field['name'] for field in json.loads(getSchemaFields(table_name))][4:]
    thresholds = getThresholds(table_name)  
    features = defaultdict(list)
    for task in tasks: 
        for col in columns:
            normed = normalize(task, col, thresholds[task])
            features[task].append(normed)
            
            '''
z='''
            qsCol = "SELECT {0} FROM [data.{1}] WHERE task='{2}'".format(col, table_name, task)
            results = queryGoogle(qsCol)
            feature = (np.array([[float(field['v']) for field in row['f']]for row in results['rows']]))
            lowNormT = float(thresholds[task][col]['lowNorm'])
            highNormT = float(thresholds[task][col]['highNorm'])
            normal = (feature - lowNormT)* (2/(highNormT-lowNormT)) - 1
            print 'This is normal:::\n', normal[:10]
            df = pd.DataFrame(normal, columns=[col])'''
q='''          
            features.join(df, how='outer')
            print features.head()
            print features.shape
                
    

    return features'''
    
#x = normalizeTimData()
#print x[:10]

# <codecell>



def qOutliers(task, table_name, thresholds=None, columns=None):
    thresholds = thresholds if thresholds else {task: getThresholds(table_name, task)}
    columns = columns if columns else [field['name'] for field in json.loads(getSchemaFields(table_name))]
    sensors = columns[4:]
    SELECT = ("SELECT ") #+ (', '.join(columns[:4])) + ',' 
    select = [] 
    FROM = (" FROM [data."+ table_name +"] ")
    WHERE = ("WHERE task='{0}' AND ".format(task))
    where = []
    for sensor in sensors:
        select.append(sensor)
        if abs(float(thresholds[task][sensor]['lowNorm']) - float(thresholds[task][sensor]['highNorm'])) > 0.01 or \
           abs(float(thresholds[task][sensor]['lowOutlier']) - float(thresholds[task][sensor]['highOutlier'])) > 0.01:
            where.append("({0} > {1} AND {0} < {2})\n".format(sensor, 
                                                             thresholds[task][sensor]['lowOutlier'], 
                                                             thresholds[task][sensor]['highOutlier']))
    
    return SELECT + (', '.join(select)) + FROM + WHERE + ' AND '.join(where) 

#print qOutliers('cutting', 'timdata')

# <codecell>

def getThresholds(table_name, task_type=None):
    #sensors = getSensors(table_name)
    thresholds = defaultdict(lambda: defaultdict(dict))
    data = queryTableData('data', 'thresholds')
    
    for row in data['rows']:
        cells = row['f']
        task = cells[0]['v']
        ttype = cells[2]['v']
        sensor = cells[3]['v']
        thresholds[task][sensor][ttype] = cells[4]['v']
    if task_type:
        return thresholds.get(task_type, 'ERROR: task not found')
    
    return thresholds

# <markdowncell>

# ##Upload TimData
# upload tim's data from his thesis

# <codecell>

import glob
import time
def uploadTim():
    table_name = 'timdata'
    fields = getSchemaFields(table_name).replace('-', '')
    def task_parse(name):
        n = name.lower()
        if 'suturing' in n: return 'suturing'
        if 'pegtx' in n or 'pegboard' in n: return 'pegtransfer'
        if 'cutting' in n: return 'cutting'
        return 'unknown'
    #data = fetchLocalData('/home/ubuntu/simulab/data/CSVs', task_parse)
    #data = open('timdata_csv_387').readlines()
    file_names = glob.glob('/home/ubuntu/simulab/small*')
    print 'got data', len(file_names), ' files'
    #print file_names
    for fname in file_names:
        with open(fname) as data:
            print fname, '...',
            body = getBody(data.read(), fields, table_name, dataset
                                  , createDisposition='CREATE_IF_NEEDED'
                                  , writeDisposition='WRITE_APPEND')
    
            loadTableFromCSV(body)
        print 'uploaded'
        time.sleep(120)
#uploadTim()

# <markdowncell>

# #FETCH:  
# 
# Fetches all data from Google BigQuery or Amazon s3
# Code to connect, clean, shape
# and move data

# <markdowncell>

# ##Fetch-Local
# amalgamates all files in a local directory and prepares for upload into google bigquery

# <codecell>

import glob
import os
import cStringIO 


def fetchLocalData(path, task_parse):
    globPath = path + '/*'
    data = open('timdata_csv_387', 'w+')#cStringIO.StringIO()
    file_names = glob.glob(globPath)
    print len(file_names)
    for fname in file_names:
        fkey = fname[:-4]
        task = task_parse(fname)
        fdate = '2012-08-30'
        with open(fname) as fin:
            for line in fin.readlines():
                if line.strip():
                    data.write('{0},{1},{2},{3}\n'.format(fkey, task, fdate, line.strip()))
    data.seek(0)
    return data
    
    


# <markdowncell>

# ##Fetch-Google

# <codecell>

projectId = '459512762119'
dataset = 'data'
url = "https://www.googleapis.com/upload/bigquery/v2/projects/" + projectId + "/jobs"

# <markdowncell>

# ###Query using BigQuery syntax

# <markdowncell>

# 
# {'rows': []}
# job complete
# current length:  10
# 1
# 10
# {'rows': [{u'f': [{u'v': u'-0.432'}, {u'v': u'3.655'}]}, {u'f': [{u'v': u'-0.432'}, {u'v': u'3.655'}]}, {u'f': [{u'v': u'-0.432'}, {u'v': u'3.655'}]}, {u'f': [{u'v': u'-0.432'}, {u'v': u'3.655'}]}, {u'f': [{u'v': u'-0.432'}, {u'v': u'3.655'}]}, {u'f': [{u'v': u'-0.432'}, {u'v': u'3.655'}]}, {u'f': [{u'v': u'-0.432'}, {u'v': u'3.655'}]}, {u'f': [{u'v': u'-0.432'}, {u'v': u'3.655'}]}, {u'f': [{u'v': u'-0.432'}, {u'v': u'3.655'}]}, {u'f': [{u'v': u'-0.432'}, {u'v': u'3.655'}]}]}

# <codecell>

def queryGoogle(queryString, http=None):  
    http = http if http else httpGoogle()
    data = {'rows': []}
    timeout = 70000 
    service = build("bigquery", "v2", http=http)
    jobCollection = service.jobs()
    queryData = {'query': queryString,
                 'timeoutMs': timeout,
                 'maxResults': 100000}
    try:
        queryReply = jobCollection.query(projectId=projectId,
                                         body=queryData).execute()
        
        jobReference=queryReply['jobReference']
        #print jobReference['jobId']
        #print projectId
        # Timeout exceeded: keep polling until the job is complete.
        while(not queryReply['jobComplete']):
            print 'Job not yet complete...'
            queryReply = jobCollection.getQueryResults(
                              projectId=jobReference['projectId'],
                              jobId=jobReference['jobId'],
                              timeoutMs=timeout).execute() 
            print projectId, ':', jobId
            print 'job complete'
        #get first page of results
        if('rows' in queryReply):
                data['rows'].extend(queryReply['rows'])
                currentRow = len(queryReply['rows'])
                print 'current length: ', currentRow
        #check for additional pages   
        i = 0
        while('rows' in queryReply and currentRow < queryReply['totalRows']):
            i += 1
            print i, 
            queryReply = jobCollection.getQueryResults(
                         projectId=jobReference['projectId'],
                         jobId=jobReference['jobId'],
                         startIndex=currentRow).execute()
            
            if('rows' in queryReply):
                data['rows'].extend(queryReply['rows'])
                currentRow += len(queryReply['rows'])
                print 'current row: ', currentRow
        print 'returning data'
        return data
        print ("The credentials have been revoked or expired, please re-run"
        "the application to re-authorize")
    
    except HttpError as err:
        print 'Error in runSyncQuery:', pprint.pprint(err.content)
    
    except Exception as err:
        print 'Undefined error: ',  err


#x= queryGoogle(qs)

# <markdowncell>

# ###Dump entire table into rows

# <codecell>

def queryTableData(dataset, table, startIndex=0, http=None):
    http = http if http else httpGoogle()
    data = {'rows': []}
    service = build("bigquery", "v2", http=http)
    tableDataJob = service.tabledata()
    try:
        queryReply = tableDataJob.list(projectId=projectId,
                                     datasetId=dataset,
                                     tableId=table,
                                     startIndex=startIndex).execute()
        
        # When we've printed the last page of results, the next
        # page does not have a rows[] array.
        while 'rows' in queryReply:
            data['rows'].extend(queryReply['rows'])
            startIndex += len(queryReply['rows'])
            queryReply = tableDataJob.list(projectId=projectId,
                                     datasetId=dataset,
                                     tableId=table,
                                     startIndex=startIndex).execute()
            
        return data
    except HttpError as err:
        print 'Error in querytableData: ', pprint.pprint(err.content)
        
#print queryTableData('data', 'thresholds')

# <markdowncell>

# ###Upload data to table using csv file

# <codecell>

def loadTableFromCSV(bodydata, http=None):
    http = http if http else httpGoogle()
    headers = {'Content-Type': 'multipart/related; boundary=xxx'}
    res, content = http.request(url, method="POST", body=bodydata, headers=headers)
    print str(res) + "\n"
    print content

# <markdowncell>

# ##Fetch-Authorization:

# <codecell>

def httpGoogle(storage_location='bigquery_web.dat' ):
    storage = Storage(storage_location) 
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        print '''There is a manual step to updating credentials.
                 Please follow Reauthorize instructions
              ''' 
    
    return credentials.authorize(httplib2.Http())



# <markdowncell>

# #Utilities:

# <markdowncell>

# ##Google

# <markdowncell>

# ###Fetch fields from schema table

# <codecell>

def getSchemaFields(table_name):
    queryString = "SELECT field_name, field_type, field_order FROM [data.schemata] WHERE table_name = '{0}' ORDER BY field_order".format(table_name)
    results = queryGoogle(queryString)
    fields = ['{{"name":"{0}", "type":"{1}"}}'.format(row['f'][0]['v'].strip(), row['f'][1]['v'].strip()) for row in results['rows']]
    return  str(('\n            \t[') + (',\n            \t'.join(fields)) + ('\n            \t]'))

# <markdowncell>

# ###Create Schemata 
# create schema table from schemat.dat
# ***Will truncate so append schemata.dat only***

# <codecell>

def createSchemata(path='/home/ubuntu/simulab/data/schemata.dat'):
    datafile = open(path).read()

    fields = '''[ 
              {"name" : "field_order", "type" : "INTEGER"}
            , {"name" : "table_name",  "type" : "STRING"}
            , {"name" : "field_name",  "type" : "STRING"}
            , {"name" : "field_type",  "type" : "STRING"}
                  ]'''
    body = getBody(datafile, fields, 'schemata', 'data', 'CREATE_IF_NEEDED' , 'WRITE_TRUNCATE')
    loadTableFromCSV(body)
    return body

#x = createSchemata()
#print x

# <markdowncell>

# ###Create table schema and body of request

# <codecell>

def getBody(data, fields, table, dataset, createDisposition, writeDisposition):
    bodyEnd = ('\n--xxx--\n')
    strbody = '''--xxx
Content-Type: application/json; charset=UTF-8

{
   "configuration": {
      "load": {
         "schema": {
            "fields" : %s
         },
         "destinationTable": {
            "projectId": "%s", 
            "datasetId": "%s",
            "tableId": "%s" 
            
         }, 
         "createDisposition": "%s", 
         "writeDisposition": "%s",
         "fieldDelimiter": ","
      }
   }
}
--xxx
Content-Type: application/octet-stream

''' %(fields, projectId, dataset, table, createDisposition, writeDisposition)

    return (strbody) + (data) + bodyEnd

# <markdowncell>

# ##Reauthorize (Create valid credentials):
# Google's authentication scheme doesn't work on text based browser (it does and is extremely painful)
# To create the credentials it's much easier to fake them out (fakie).  
# The fakie string below contains the string representation of stored (json) authentication keys.  Once   
# created these credentials should work on any machine for any purpose designated by the google console  
# (web, installed device)
# In order to create new credentials you will need access to:  
# 1. [Google API Console](https://code.google.com/apis/console)   
# 2. [OAuth Playground](https://developers.google.com/oauthplayground)   
# 3. rich browser (chrome).
# 
# *[Google Blog walk-through](http://googleappsdeveloper.blogspot.com/2011/09/python-oauth-20-google-data-apis.html)

# <markdowncell>

#          

# <markdowncell>

# ####Google Setup:  
# 1. If the appropriate client id does not exsit, in the [Google API Console](https://code.google.com/apis/console):
# 
#      1.  Click Create Another Client ID  
#      1.  Select 'Web Application' for web access /  Installed Applications  for console apps just select Other and ok.  
#      1.  Update the default to https://localhost:8888/oauth2callback for web access / click 'Other' for console apps  
#      1.  Click ok  
# 
# 1. From the [Google API Console](https://code.google.com/apis/console) update variables:
#      *  client_id  
#      *  client_secret  
#      *  redirect_uri 

# <markdowncell>

# ####Authorization  
# 1.  Run the code below
# 1.  Paste auth_uri into rich browser
#     1.  Authorize simscore
#     1.  Click through any SSL certification errors
#     1.  Copy code from address bar (after code=)
#     1.  Paste the value into the variable code below
# 1.  Run the code below again
# 
# You should now be authenticated.  The storage_location under global variables holds the credentials files read in by all the functions.  If you change this then other functions won't be able to find the credentials file saved by this.

# <codecell>

#This token only works once.
code = '4/Q1Fc8XZ5NDKZAn3AUk9b6pKhv2b0.Qn7hMbdRNIYXuJJVnL49Cc8oCnj6cgI'


client_id = '459512762119-hnjnbr6nilcuib72ig1tk4pom3bfefgr.apps.googleusercontent.com'
client_secret = 'gIy7bJaFm6CRX7cXUoCQdB74'
redirect_uri = 'https://localhost:8888/oauth2callback'
scope = 'https://www.googleapis.com/auth/bigquery'
token_uri='https://accounts.google.com/o/oauth2/token'
def get_credentials():
    flow = OAuth2WebServerFlow(client_id=client_id,
                              client_secret=client_secret,
                              scope=scope,
                              redirect_uri=redirect_uri)
    flow.params['access_type'] = 'offline'
    flow.params['approval_prompt'] = 'force'

    auth_uri = flow.step1_get_authorize_url(redirect_uri)
    print 'auth_uri: \n', auth_uri #navigate to uri authorize and update code above. then rerun this.  You should be authenticated.
    
    credential = flow.step2_exchange(code)
        
    storage = Storage(storage_location) 
    storage.put(credential)
    credential.set_store(storage)
    print 'Authentication successful.'

    return credential

