# Evaluation-metrics
This is the evaluation code for cardiac MRI prediction with given metrics.


# How to use
Prepare your prediction masks and the ground truth masks as the following instructions. Then in the "main.py" define your mask paths by the variables "pathPrediction" and "pathGT", and specify the class you want to evaluate by the varibale "label". You can save your result on .csv by uncommenting the last section.

You may need to install some dependencies by:

	pip install SimpleITK
	pip install scipy


# Metrics
Evaluation of the myocardium segmentation: the Dice, the difference of the volumes, and the Hausdorff distance will be calculated between the grand truth and the prediction.

Evaluation of the scar tissues including the myocardial infarction and the No-Reflow: the Dice, the difference of the volumes, and the difference rate of the volumes.

The Dice is calculated firstly on each slice (2D), then the Dice of the case is the average of all the slices. 

The difference of the volumes between the GT and the prediction is the absolute difference between the prediction volume and the GT volume. The voxel spacing is taken into account and the unit is mm³.

The difference rate of the volumes between the GT and the prediction is calculated as the (difference of the scar tissue volume)/(myocardium volume). This metric can describe more objectively the scar tissue prediction's quality.


#  Files organization
The default file organization should be similar to the dataset.
You should have 2 folders to put your predictions and the corresponding GTs. Both of them should have the same organization.
For example,

root / GT / CaseX / Contours / CaseX.nii.gz

root / prediction / CaseX / Contours / CaseX.nii.gz	

#  Mask file format and encoding
This code loads the prediction and the GT mask from nifti files by default. You should take the contour nifti files from the dataset as the GT. Your prediction mask should have the same encoding as the mask in the dataset, that is: the mask should be encoded as catagorical labels from 0 to 4. The label and the class are {"background":0 ,"cavity":1, "normal_myocardium":2, "infarction":3, "NoReflow":4}. Notice that to evaluate the prediction of the myocardium, the mask labels should be the ensemble of 2,3 and 4.
