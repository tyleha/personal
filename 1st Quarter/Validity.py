# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

%load_ext autoreload
%autoreload 2
import numpy as np
import json
#import fetchS3
import cStringIO
from operator import itemgetter
from collections import defaultdict, namedtuple
from datetime import datetime
#from configuration import formats
#from configuration import converterdict
#from configuration import metafields, MetadatFieldNames

# <codecell>

{u'EdgeUnitId': 6, u'ForwardKinematicsMatrixLeft': u'-0.06102 0.57388 -0.81667 -6.45954 -0.81560 0.44299 0.37223 -14.73327 0.57538 0.68879 0.44102 14.55966 0.00000 0.00000 0.00000 1.00000', u'EdgeToolIdRight': 64, u'MD5HashVideo': u'244b5d5e08f3bdcf2aea18239a0a5f8f', u'IsCalibrationTrace': False, u'CaptureResult': u'None', u'EdgeToolIdRightHex': u'00000040', u'VideoFileNameOnS3': u'edge6/2012/10/24.21.59.05.325.0.mp4', u'EdgeUnitName': u'Edge Unit Name', u'MetaDataFileNameOnS3': u'edge6/2012/10/24.21.59.05.325.0.log', u'ForwardKinematicsMatrixRight': u'-0.05939 0.57102 -0.81883 6.68960 0.83328 -0.42326 -0.35565 -14.68017 -0.54962 -0.70341 -0.45085 14.02663 0.00000 0.00000 0.00000 1.00000', u'ProctorPegTransfer': {u'NonMidAirTransferBetweenHands': False, u'DroppedOutsideTaskRegion': False, u'InstrumentLeftFieldOfView': False, u'NumberDropped': 0}, u'VideoCapturedFrameCount': 4558, u'ProctorSuture': {u'AirKnot': False, u'AvulseModelFromBoard': False, u'EdgesAreNotApproximatedCloselyTogether': False, u'DroppedNeedle': False, u'BrokeSutureOrBentNeedle': False, u'BunnyEar': False, u'BrokeSuture': False, u'InstrumentLeftFieldOfView': False, u'BuckledPenrose': False, u'LessThan3KnotThrows': False, u'DistanceFromTargetDot': 0, u'BentNeedle': False, u'DistanceFromTargetDotRight': 0, u'DistanceFromTargetDotLeft': 0, u'CanSlideOpen': False}, u'DataFileTotalBytes': 1015558, u'UserId': 325, u'MD5HashData': u'7a232783afb2a4d052c06e93e7a86a1c', u'EdgeToolIdLeftHex': u'40000014', u'MetaDataFileTotalBytes': 4383, u'MetaDataFileUploadTimeSeconds': 0, u'DataFileNameOnEdge': u'C:\\Edge\\DATA\\2012.10.24.21.59.05.325.0.txt', u'VideoDroppedFrameCount': 1, u'ProctorCutting': {u'LeftToolIsScissors': False, u'NumberOfTimesOutsideTheLine': 0, u'ScissorTipsNotPointedToInterior': False, u'AvulseTissueFromClamps': False, u'InstrumentLeftFieldOfView': False, u'CuttingOutsideLines': False, u'ToreOrPokedHole': False}, u'DataFileUploadRetryCount': 0, u'CalibrationData': {u'L_ROT': {u'HomeValue': -227, u'MaxValue': 2321, u'MinValue': -4376}, u'L_J1': {u'HomeValue': 94, u'MaxValue': 774, u'MinValue': 68}, u'R_J2': {u'HomeValue': 618, u'MaxValue': 906, u'MinValue': 50}, u'R_J1': {u'HomeValue': 820, u'MaxValue': 843, u'MinValue': 169}, u'L_J2': {u'HomeValue': 360, u'MaxValue': 912, u'MinValue': 64}, u'R_ThG': {u'HomeValue': 0, u'MaxValue': 0, u'MinValue': 0}, u'EdgeMachineIdWhichPerformedCalibration': 6, u'CalibrationSavedDate': u'2012-05-30T14:55:29.433', u'R_LIN': {u'HomeValue': 0, u'MaxValue': 0, u'MinValue': 0}, u'L_LIN': {u'HomeValue': 18, u'MaxValue': 2742, u'MinValue': -4301}, u'R_Fg': {u'HomeValue': 0, u'MaxValue': 0, u'MinValue': 0}, u'L_ThG': {u'HomeValue': 174, u'MaxValue': 293, u'MinValue': 101}, u'R_ROT': {u'HomeValue': 0, u'MaxValue': 0, u'MinValue': 0}, u'L_Fg': {u'HomeValue': 55, u'MaxValue': 369, u'MinValue': 84}}, u'ClrSoftwareVersion': u'4.0.30319.269', u'ProctorId': 288, u'ProctorCancelledTest': False, u'ProctorClipApply': {u'CrossingClips': False, u'FailedToPutMinimum2ClipsBetweenLines': False, u'InstrumentLeftFieldOfView': False, u'StraightCutOnMiddleDottedLine': False, u'IncompleteCoaption': False, u'GraspedTheRenalArtery': False, u'FailedToPut4Clips': False}, u'MD5HashMetadata': u'dacc6c4fdcea318ecd0dd0c5778c37e8', u'VideoFileUploadRetryCount': 0, u'UploadResult': 0, u'MetaDataFileUploadRetryCount': 0, u'EdgeToolIdLeft': 1073741844, u'VideoFileUploadTimeSeconds': 0, u'EdgeSoftwareVersion': u'1.6.0.0', u'DataFileUploadTimeSeconds': 0, u'TestDurationInSeconds': 152.1457022, u'Id': 105, u'DataFileNameOnS3': u'edge6/2012/10/24.21.59.05.325.0.txt', u'VideoFileNameOnEdge': u'C:\\Edge\\VIDEO\\2012.10.24.21.59.05.325.0.mp4', u'TaskId': 0, u'TaskUploadProgress': 5, u'IsPracticeTest': False, u'MetaDataFileNameOnEdge': u'C:\\Edge\\DATA\\2012.10.24.21.59.05.325.0.log', u'VideoFileTotalBytes': 31619141}

# <codecell>


# <codecell>

import json
json_data= open('C:\Users\Tyler\Downloads\\21.15.46.57.288.2.log')
meta = json.load(json_data)
json_data.close()

'''#########################
Compute Test Summary Metrics
#########################'''

#TestID	Int	The uniquely generated ID for this test score to associate all other data with.
TestID = meta['DataFileNameOnS3'][:-4]
#IsPractice	Boolean	Is this a scored test?
IsPractice = meta["IsPracticeTest"]
#UploadDate	String	Upload Date

#UploadDateUnix	Time	Date converted into Unix Epoch C Time for fast sorting.

#MetadataFilename	String	Metadata Filename and location in S3.
MetadataFilename = meta["MetaDataFileNameOnS3"]
#TestDataFilename	String	Test Data Filename and location in S3.
TestDataFilename = meta['DataFileNameOnS3']
#VideoDataFilename	String	Video Data Filename and location in S3.
VideoDataFilename = meta["VideoFileNameOnS3"]
#UserID	String	User ID.
UserID = str(meta['UserId'])
#ProctorID	String	Proctor ID.
ProctorID = str(meta["ProctorId"])
#EdgeID	String	EDGE ID.
EdgeID = str(meta["EdgeUnitId"])
#InstitutionID	String	EDGE Institution ID.
inst = ['Engineering','Tulane','SIU','UPMC','Madigan','Duke','UC Irvine','UNM','Cleveland Clinic','UW','OSU','NA','NA']
try: InstitutionID = inst[meta['EdgeUnitId']]
except: InstitutionID = 'Unknown'
#SwVersion	String	EDGE software version.
SwVersion = meta["EdgeSoftwareVersion"]
#RToolID	String	Right Tool ID.
RToolID = meta["EdgeToolIdRight"]
LToolID = meta["EdgeToolIdLeft"]
#TestLength	String	The length of time it took to complete the task. Ex: 02:00.0.
TestLength = meta["TestDurationInSeconds"]
#TaskType	String	Task Type.
tasks = ['PegTransfer','Cutting','Suture','ClipApply']
try: TaskType = tasks[meta["TaskId"]]
except: TaskType = 'Unknown'
#Badframe	Int	Video dropped frame count.

#FailType	String	Concatenated string of items that failed. Ex: OB Data, Video Corruption

#BadSensors	String	Concatenated string of sensors that are bad. Ex: J1_R, Fg_L.

# <codecell>

'''#########################
Compute Test Data Metrics
#########################'''

# <codecell>

'''###########################
Compute Machine Health Metrics
###########################'''

