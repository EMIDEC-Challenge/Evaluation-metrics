#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 20:36:27 2020

@author: chen
"""
import metrics

import numpy
from scipy.ndimage import _ni_support
from scipy.ndimage.morphology import distance_transform_edt, binary_erosion,\
    generate_binary_structure
from scipy.ndimage.measurements import label, find_objects
from scipy.stats import pearsonr
import os
import os
import shutil
from time import time

import numpy as np
import SimpleITK as sitk
import scipy.ndimage as ndimage

###**************Load predicted and GT mask as a volume***********************

#path of your prediction and GT floder
#The prediction mask and GT mask should have a same or similar name. 
pathPrediction="prediction"
pathGT="GT"
label={"cavity":1, "normal_myocardium":2, "infarction":3, "NoReflow":4}
dice=[]
jaccard=[]
HD95=[]
HD=[]
relativeAbsoluteVolumeDifference=[]
averageSymmetricSurfaceDistance=[]
averageSurfaceDistance=[]
sensitivity=[]
specifity=[]
precision=[]
recall=[]
volumeCorrelation=[]
volumeOverDifference=[]
volumeChangeCorrelation=[]
trueNegativeRate=[]
truePositiveRate=[]
volumeDifference=[]
for filePrediction in os.listdir(pathPrediction):
    #  load prediction mask as a nifiti, you can use nib.load as well for nifti
    prediction = sitk.ReadImage(os.path.join(pathPrediction, filePrediction), sitk.sitkInt16) 
    #  the prediction mask array should be one hot format
    predArray = sitk.GetArrayFromImage(prediction)  # convert into numpy array

    # load GT mask. 
    # You should modify the GT file name if its name is different to the prediction file
    GT = sitk.ReadImage(os.path.join(pathGT, filePrediction), sitk.sitkInt8) 
    GTArray = sitk.GetArrayFromImage(GT)
    spacing=GT.GetSpacing()
    #  get the one hot GT mask of the indexing class
    GTArray = GTArray==label["cavity"]
    predArray = predArray==label["cavity"]
    predArray[1:3] = np.zeros_like(predArray[1:3])
    ###*****************choose the metrics to calculate*****************
    dice.append(metrics.dc(predArray, GTArray))
    jaccard.append(metrics.jc(predArray, GTArray))
    HD95.append(metrics.hd95(predArray, GTArray))
    HD.append(metrics.hd(predArray, GTArray))
    
    relativeAbsoluteVolumeDifference.append(metrics.ravd(predArray, GTArray))
    averageSymmetricSurfaceDistance.append(metrics.assd(predArray, GTArray, voxelspacing=spacing))
    averageSurfaceDistance.append(metrics.asd(predArray, GTArray, voxelspacing=spacing))
    
    sensitivity.append(metrics.sensitivity(predArray, GTArray))
    specifity.append(metrics.specificity(predArray, GTArray))
    precision.append(metrics.precision(predArray, GTArray))
    recall.append(metrics.recall(predArray, GTArray))
    
    volumeCorrelation.append(metrics.volume_correlation(predArray, GTArray)[1])
    volumeOverDifference.append(metrics.volumeofff(predArray, GTArray))
    volumeChangeCorrelation.append(metrics.volume_change_correlation(predArray, GTArray))
    
    trueNegativeRate.append(metrics.true_negative_rate(predArray, GTArray))
    truePositiveRate.append(metrics.true_positive_rate(predArray, GTArray))
    
    volumeDifference.append(abs(metrics.volume(predArray, spacing)-metrics.volume(GTArray, spacing)))


np.savetxt('csv/dice.csv', dice, delimiter=',', fmt='%f')
np.savetxt('csv/jaccard.csv', jaccard, delimiter=',', fmt='%f')
np.savetxt('csv/HD95.csv', HD95, delimiter=',', fmt='%f')
np.savetxt('csv/HD.csv', HD, delimiter=',', fmt='%f')    

np.savetxt('csv/ASD.csv', averageSurfaceDistance, delimiter=',', fmt='%f')  
np.savetxt('csv/ASSD.csv', averageSymmetricSurfaceDistance, delimiter=',', fmt='%f') 
np.savetxt('csv/RAVD.csv', relativeAbsoluteVolumeDifference, delimiter=',', fmt='%f')

np.savetxt('csv/specifity.csv', specifity, delimiter=',', fmt='%f')
np.savetxt('csv/sensitivity.csv', sensitivity, delimiter=',', fmt='%f')
np.savetxt('csv/precision.csv', precision, delimiter=',', fmt='%f')

np.savetxt('csv/VOE.csv', volumeOverDifference, delimiter=',', fmt='%f')
np.savetxt('csv/VC.csv', volumeCorrelation, delimiter=',', fmt='%f') 
np.savetxt('csv/VCC.csv', volumeChangeCorrelation, delimiter=',', fmt='%f')    
    
np.savetxt('csv/TPR.csv', truePositiveRate, delimiter=',', fmt='%f') 
np.savetxt('csv/TNR.csv', trueNegativeRate, delimiter=',', fmt='%f') 

np.savetxt('csv/volume.csv', volumeDifference, delimiter=',', fmt='%f')

avgDice = float(sum(dice))/len(dice)
avgJaccard= float(sum(jaccard))/len(jaccard)
avgHd95 = float(sum(HD95))/len(HD95)
avgHd= float(sum(HD))/len(HD)
avgSpecifity = float(sum(specifity))/len(specifity)
avgSensitivity= float(sum(sensitivity))/len(sensitivity)
avgVOE = float(sum(volumeOverDifference))/len(volumeOverDifference)
avgVC= float(sum(volumeCorrelation))/len(volumeCorrelation)
avgASSD = float(sum(averageSymmetricSurfaceDistance))/len(averageSymmetricSurfaceDistance)
avgRAVD= float(sum(relativeAbsoluteVolumeDifference))/len(relativeAbsoluteVolumeDifference)


    
    
    