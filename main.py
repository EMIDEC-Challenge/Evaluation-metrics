#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 20:36:27 2020

@author: chen
"""
import metrics

import numpy as np
import os
import shutil
import SimpleITK as sitk
import scipy.ndimage as ndimage

###**************Load predicted and GT mask as a volume***********************

#path of your prediction and GT floder
#The prediction mask and GT mask should have a same or similar name. 
pathPrediction="prediction"
pathGT="GT"

dice=[]
HD=[]
volumeDifference=[]
volumeDifferenceRate=[]
volumePrediction=[]

#class index in GT contour nifti{"background":0 ,"cavity":1, "normal_myocardium":2, "infarction":3, "NoReflow":4}
#*********************************************
#choose the tissue class you want to calculate here
#label=("Myocardium", "Infarction", "No Reflow")
label="No Reflow"
#*********************************************

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
    
    #  get the one hot GT mask of the indexed class
    if label=="Myocardium": #The Myocardium includes both the normal myocardium and scar tissue
        aGTArray = (GTArray==2) + (GTArray==3) + (GTArray==4)
        aPredArray = (predArray==2) + (predArray==3) + (predArray==4)
        #aPredArray[1:3] = np.zeros_like(aPredArray[1:3])
        
    elif label=="Infarction":
        aGTArray = GTArray==3
        aPredArray = predArray==3
        #aPredArray[1:3] = np.zeros_like(aPredArray[1:3])
        
    elif label=="No Reflow":
        aGTArray = GTArray==4
        aPredArray = predArray==4
        #aPredArray[1:3] = np.zeros_like(aPredArray[1:3])
    else:
        raise NameError('Unknown class name')
    ###*****************metrics calculation*****************
    ###*****************commun metrics******************
    dice.append(metrics.dc(aPredArray, aGTArray))
    aVolumePred=metrics.volume(aPredArray, spacing)
    aVolumeGT=metrics.volume(aGTArray, spacing)
    volumePrediction.append(aVolumePred)
    volumeDifference.append(abs(aVolumePred-aVolumeGT))
    
    ###****************metric for myocardium***********
    if label=="Myocardium":
        HD.append(metrics.hd(predArray, GTArray))
        
    ###****************metric for scar tissues***********
    else:
        aVolumeMyo=metrics.volume((GTArray==2) + (GTArray==3) + (GTArray==4), spacing)
        volumeDifferenceRate.append(abs(aVolumePred-aVolumeGT)/aVolumeMyo)
        


    

avgDice = float(sum(dice))/len(dice)
avgVD= float(sum(volumeDifference))/len(volumeDifference)
if label=="Myocardium":
    avgHd= float(sum(HD))/len(HD)
else:
    avgVDR= float(sum(volumeDifferenceRate))/len(volumeDifferenceRate)

'''
#comment the csv you don't want to save
np.savetxt('csv/dice.csv', dice, delimiter=',', fmt='%f')
np.savetxt('csv/HD.csv', HD, delimiter=',', fmt='%f')    
np.savetxt('csv/volumeDif.csv', volumeDifference, delimiter=',', fmt='%f')
np.savetxt('csv/volume.csv', volumePrediction, delimiter=',', fmt='%f')
np.savetxt('csv/volumeDifRate.csv', volumeDifferenceRate, delimiter=',', fmt='%f')
'''



    
    
    