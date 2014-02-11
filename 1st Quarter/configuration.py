# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
from collections import namedtuple
ranges = {
			'%Time_V1'	: {'min': 0., 'max': None }
			, 'J1_L'  	: {'min': 0., 'max': 105. }
			, 'J2_L'  	: {'min': 0., 'max': 120. }
			, 'Lin_L' 	: {'min': 0., 'max': 14. }
			, 'Rot_L' 	: {'min': 0., 'max': 360. }
			, 'ThG_L'	: {'min': -50., 'max': 50. }
			, 'Fg_L'	: {'min': -20., 'max': 125. }
			, 'J1_R'	: {'min': 0., 'max': 105. }
			, 'J2_R'	: {'min': 0., 'max': 120. }
			, 'Lin_R'	: {'min': 0., 'max': 14. }
			, 'Rot_R'	: {'min': 0., 'max': 360. }
			, 'ThG_R'	: {'min': -50., 'max': 50. }
			, 'Fg_R'	: {'min': -20., 'max': 125. }
			, 'X_L'		: {'min': -26., 'max': 26. }
			, 'Y_L'		: {'min': -3., 'max': 15. }
			, 'Z_L'		: {'min': -8., 'max': 2. }
			, 'X_R'		: {'min': -26., 'max': 26. }
			, 'Y_R'		: {'min': -3., 'max': 15. }
			, 'Z_R'		: {'min': -8., 'max': 2. }
		}

isClipTask = lambda f: True if f[-5 :]=='3.txt' else False
stringNaN = lambda m: 'NaN' if np.isnan(m) else m

rating = lambda t: 'fail' if t else 'pass'

conf =  lambda x: testnan(x)

toolRight = "EdgeToolIdRight"
toolLeft = "EdgeToolIdLeft"

def testnan(x):
    try:
        float(x)
        return x
    except:
        return np.NaN

names = ['%Time_V1', 'J1_L', 'J2_L', 'Lin_L', 'Rot_L', 'ThG_L', 'Fg_L', 'J1_R', 'J2_R', 'Lin_R', 'Rot_R', 'ThG_R', 'Fg_R', 'X_L', 'Y_L', 'Z_L', 'X_R', 'Y_R', 'Z_R']
formats = [np.float, np.float, np.float, np.float, np.float, np.float, np.float, np.float, np.float, np.float, np.float, np.float, np.float, np.float, np.float, np.float, np.float, np.float, np.float]
dtype = {'names' : names, 'formats' : formats}
converterdict = {0: conf, 1: conf, 2: conf, 3: conf, 4: conf, 5: conf, 6: conf, 7: conf, 8: conf, 9: conf, 10: conf, 11: conf, 12: conf, 13: conf, 14: conf, 15: conf, 16: conf, 17: conf, 18: conf}

sensors = {'J1'  : ('J1_L', 'J1_R')
		 , 'J2'  : ('J2_L', 'J2_R') 
		 , 'Lin' : ('Lin_L', 'Lin_R')
		 , 'Rot' : ('Rot_L', 'Rot_R')
		 , 'ThG' : ('ThG_L', 'ThG_R')
		 , 'Fg'  : ('Fg_L', 'Fg_R')
		 , 'X'   : ('X_R', 'X_R')
		 , 'Y'   : ('Y_R', 'Y_R')
		 , 'Z'   : ('Z_R', 'Z_R')}

pSuture = ['InstrumentLeftFieldOfView', 'DistanceFromTargetDot', 'BuckledPenrose',
           'LessThan3KnotThrows','CanSlideOpen', 'AirKnot', 'BunnyEar',
           'AvulseModelFromBoard', 'BrokeSutureOrBentNeedle', 'DroppedNeedle']

pPegTransfer = ['InstrumentLeftFieldOfView', 'NumberDropped',
				'NonMidAirTransferBetweenHands','DroppedOutsideTaskRegion']

pCutting = ['InstrumentLeftFieldOfView', 'CuttingOutsideLines',
			 'ToreOrPokedHole', 'ScissorTipsNotPointedToInterior',
			 'AvulseTissueFromClamps', 'LeftToolIsScissors']

pClipApply = ['InstrumentLeftFieldOfView', 'FailedToPutMinimum2ClipsBetweenLines',
			  'FailedToPut4Clips', 'IncompleteCoaption', 'CrossingClips',
		 	 'StraightCutOnMiddleDottedLine', 'GraspedTheRenalArtery']
MetadatFieldNames = {'ProctorSuture' : ["AirKnot","AvulseModelFromBoard","EdgesAreNotApproximatedCloselyTogether",
									    "DroppedNeedle","BrokeSutureOrBentNeedle", "BunnyEar","BrokeSuture",
									    "InstrumentLeftFieldOfView","BuckledPenrose","LessThan3KnotThrows",
									    "DistanceFromTargetDot", "BentNeedle",
									    "DistanceFromTargetDotRight","DistanceFromTargetDotLeft",
									    "CanSlideOpen"]

                     , 'ProctorPegTransfer' : ["NonMidAirTransferBetweenHands", "DroppedOutsideTaskRegion", "InstrumentLeftFieldOfView", "NumberDropped"]

                     , 'ProctorCutting' : ["LeftToolIsScissors", "NumberOfTimesOutsideTheLine", "ScissorTipsNotPointedToInterior",
										   "AvulseTissueFromClamps", "InstrumentLeftFieldOfView", "CuttingOutsideLines", 
										   "ToreOrPokedHole"] 

                     , 'ProctorClipApply' : ["CrossingClips", "FailedToPutMinimum2ClipsBetweenLines", 
											"InstrumentLeftFieldOfView", "StraightCutOnMiddleDottedLine", 
											"IncompleteCoaption", "GraspedTheRenalArtery", "FailedToPut4Clips"]}

metafields = ['MetaDataFileNameOnS3', 'DataFileNameOnS3', 'VideoFileNameOnS3', 
              'EdgeUnitId', 'IsPracticeTest', 'IsCalibrationTrace', 'EdgeToolIdLeft',
              'EdgeToolIdRight', 'ProctorCancelledTest', 'TestDurationInSeconds', 
              'EdgeSoftwareVersion', 'ProctorSuture', 'ProctorPegTransfer', 'ProctorCutting', 
              'ProctorClipApply']

# <codecell>


