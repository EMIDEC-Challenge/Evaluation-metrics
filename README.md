# Evaluation-metrics
This is the evaluation code for cardiac MRI prediction with given metrics.


# How to use


You may need to install some dependencies by:

	pip install SimpleITK
	pip install scipy
	
To run the program, please run 
	
	python3 main.py CLASS_NAME PATH_PREDICTION PATH_GT
The CLASS_NAME should be one of ("Myocardium", "Infarction", "NoReflow"). E.g.,

	python3 main.py NoReflow prediction GT
	
Optionally, you can give only the parameter CLASS_NAME, the default prediction and GT folder path is "prediction" and "GT". E.g.,
	
	python3 main.py Myocardium
	
	
To prepare your prediction masks and the ground truth masks, please refer to the following instructions. 

# Metrics
The applied metrics depend on the class of segmented tissue. 

Evaluation of the myocardium segmentation: the Dice index, the difference of the volumes, and the Hausdorff distance will be calculated between the grand truth and the prediction.

Evaluation of the scar tissues segmentation including the myocardial infarction and the No-Reflow: the Dice index, the difference of the volumes, and the difference of the ratio (disease volume / myocardium volume).

The Dice index is calculated firstly on each slice (2D), then the Dice index of the case is the average of all the slices. 

The difference of the volumes between the GT and the prediction is the absolute difference between the prediction volume and the GT volume. The voxel spacing is taken into account and the unit is mm³.

The difference of the ratio (disease volume / myocardium volume) between the GT and the prediction is calculated as (difference of the infarction or No Reflow volume)/(myocardium volume). This metric can describe more objectively the scar tissue prediction's quality in regard to the volume of myocardium.

The code will display the mean values of the metrics depending on the class you want to evaluate. The values of each case are saved as csv files in the folder ./csv  

#  Files organization
The default file organization should be similar to the dataset.
You should have 2 folders to put your predictions and the corresponding GTs. Both of them should have the same organization.
For example,

root / GT / CaseX / Contours / CaseX.nii.gz

root / prediction / CaseX / Contours / CaseX.nii.gz	

#  Mask file format and encoding
This code loads the prediction and the GT mask from nifti files by default. You should take the contour nifti files from the dataset as the GT. Your prediction mask should have the same encoding as the mask in the dataset, that is: the mask should be encoded as categorical labels from 0 to 4. The label and the class are {"background":0 ,"cavity":1, "normal_myocardium":2, "infarction":3, "NoReflow":4}. 
Notice that to evaluate the prediction of the myocardium, the mask labels should be the ensemble of 2,3 and 4.
