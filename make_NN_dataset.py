import os
import pathlib
import numpy as np
from shutil import copy
mypath = "/home/dm3315/Documents/SK/PMT_learning/images/"
#Randomly selects images, renames them and puts them into folders for neural net
#Directory structure:   dataset ->train_frames->train
#                               ->train_masks->train
#                                ->val_frames->val
#                                ->val_masks->val
#                                ->test_frames->test
#                                ->output


#name of dataset
out_dir = 'bolts_dyn'

#number of total images for training testing and validation, multiple of 100
num_img = 200  
mkdirs = False

#get list of filenames of small images
f = []
for (dirpath, dirnames, filenames) in os.walk(f'{mypath}Raw/Surveys/IDBottomSurvey/raw_small_images/'):
    f.extend(filenames)
    break

    #make directory paths if needed
if(mkdirs == True) :
    os.mkdir(f'{mypath}datasets/{out_dir}/')
    pathlib.Path(f'{mypath}datasets/{out_dir}/train_frames/train/').mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'{mypath}datasets/{out_dir}/train_masks/train/').mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'{mypath}datasets/{out_dir}/val_frames/val').mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'{mypath}datasets/{out_dir}/val_masks/val').mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'{mypath}datasets/{out_dir}/test_frames/test').mkdir(parents=True, exist_ok=True)
    pathlib.Path(f'{mypath}datasets/{out_dir}/output').mkdir(parents=True, exist_ok=True)


#Randomly select images and remove the one that is saved
for i in range(num_img):

    rand = np.random.randint(len(f))
    if i<0.7*num_img :
        copy(f'{mypath}Raw/Surveys/IDBottomSurvey/raw_small_images/{f[rand]}', f'{mypath}datasets/{out_dir}/train_frames/train/{str(i)}.png')
    elif 0.7*num_img<=i<0.9*num_img :
        copy(f'{mypath}Raw/Surveys/IDBottomSurvey/raw_small_images/{f[rand]}', f'{mypath}datasets/{out_dir}/val_frames/val/{str(i)}.png')
    elif 0.9*num_img <= i :
        copy(f'{mypath}Raw/Surveys/IDBottomSurvey/raw_small_images/{f[rand]}', f'{mypath}datasets/{out_dir}/test_frames/test/{str(i)}.png')
    
    del f[rand]
