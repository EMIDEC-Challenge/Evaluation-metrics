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
import sys


def main():
    
    args = sys.argv[1:]
    if len(args)==0:
        label="Myocardium"
        pathPrediction="prediction"
        pathGT="GT"
    elif len(args)==3:
        label=args[0]
        pathPrediction=args[1]
        pathGT=args[2]
    elif len(args)==1:
        label=args[0]
        pathPrediction="prediction"
        pathGT="GT"
    else:
        print("Parameter error. Please check How To Use in the Readme." )
        sys.exit(0)
    

    dice=[]
    HD=[]
    volumeDifference=[]
    volumeDifferenceRate=[]
    volumePrediction=[]
    
    for filePrediction in sorted(os.listdir(pathPrediction)):
        #  load prediction mask as a nifiti, you can use nib.load as well for nifti
        prediction = sitk.ReadImage(os.path.join(pathPrediction, filePrediction, 'Contours', filePrediction+'.nii.gz'), sitk.sitkInt16) 
        #  the prediction mask array should be encoded as the categorical value from 0 to 4. 
        #  the correspendnence of the Value-Class should be the same as the GT mask 
        predArray = sitk.GetArrayFromImage(prediction)  # convert into numpy array
    
        # load GT mask. 
        # You should modify the GT file name if its name is different to the prediction file
        GT = sitk.ReadImage(os.path.join(pathGT, filePrediction, 'Contours', filePrediction+'.nii.gz'), sitk.sitkInt16) 
        GTArray = sitk.GetArrayFromImage(GT)
        spacing=GT.GetSpacing()
        #  get the one hot GT mask of the indexed class
        #class index in GT contour nifti{"background":0 ,"cavity":1, "normal_myocardium":2, "infarction":3, "NoReflow":4}
        if label=="Myocardium": #The Myocardium includes both the normal myocardium and scar tissue
            aGTArray = (GTArray==2) + (GTArray==3) + (GTArray==4)
            aPredArray = (predArray==2) + (predArray==3) + (predArray==4)
            #aPredArray[1:3] = np.zeros_like(aPredArray[1:3])
            
        elif label=="Infarction":
            aGTArray = (GTArray==3) + (GTArray==4)
            aPredArray = (predArray==3) + (predArray==4)
            #aPredArray[3:4] = np.zeros_like(aPredArray[3:4])
            
        elif label=="NoReflow":
            aGTArray = GTArray==4
            aPredArray = predArray==4
            #aPredArray[1:7] = np.zeros_like(aPredArray[1:7])
        else:
            raise NameError('Unknown class name')
        ###*****************metrics calculation*****************
        ###*****************commun metrics******************
        dice.append(metrics.dc(aPredArray, aGTArray))
        aVolumePred=metrics.volume(aPredArray, spacing)
        aVolumeGT=metrics.volume(aGTArray, spacing)
        volumePrediction.append(round(aVolumePred, 2))
        volumeDifference.append(round(abs(aVolumePred-aVolumeGT),2))
        ###****************particular metric for myocardium***********
        if label=="Myocardium":
            HD.append(metrics.hd(aPredArray, aGTArray, spacing))
    
            
        ###****************particular metric for scar tissues***********
        else:
            aVolumeMyo=metrics.volume((GTArray==2) + (GTArray==3) + (GTArray==4), spacing)
            volumeDifferenceRate.append(abs(aVolumePred-aVolumeGT)/aVolumeMyo)
            
    

    avgDice = float(sum(dice))/len(dice)
    print("Average Dice index: ", "{:.2%}".format(avgDice))
    np.savetxt('csv/Dice.csv', dice, delimiter=',', fmt='%f')
    avgVD= float(sum(volumeDifference))/len(volumeDifference)
    print("Average volume difference: ", round(avgVD, 2), "mm\N{SUPERSCRIPT THREE}")
    np.savetxt('csv/volumeDif.csv', volumeDifference, delimiter=',', fmt='%f')
    if label=="Myocardium":
        avgHd= float(sum(HD))/len(HD)
        print("Average Hausdorff distance: ", round(avgHd, 2), "mm")
        np.savetxt('csv/HD.csv', HD, delimiter=',', fmt='%f')   
    else:
        avgVDR= float(sum(volumeDifferenceRate))/len(volumeDifferenceRate)
        print("Average volume difference ratio according to volume of myocardium: ", "{:.2%}".format(avgVDR))
        np.savetxt('csv/volumeDifRatio.csv', volumeDifferenceRate, delimiter=',', fmt='%f')
    

if __name__ == "__main__":
    main()





    
    
    