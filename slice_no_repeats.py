#script chops up images in random grid pattern dropping ALL images into mypath + dir_name
import cv2
from PIL import Image
from os import walk
import numpy as np

#TODO: MAke the slicing more efficient, skipping swathes of image

# Output image size, make it divisible by 32
w = 416
h = 416
OUTPUT_SIZE = (w,h) 

#margin around edge of large image to skip unresolved pmts
CB = 500
#random movements of window to give random crops to image
cell_margin = 10

#Take input directory and cut up large images randomly to uotput to another
mypath = "/home/dm3315/Documents/SK/PMT_learning/images/IDBottomSurvey/"
dir_name = 'raw_small_images'
f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break

#remove .JPG from end of filenames
f = [x[:-4] for x in f]
obj_num = 0

for x in f :
    print(x)
    img = np.array(Image.open(f'{mypath}{x}.JPG'))
    img = img[CB:-CB,CB:-CB,:]
    
    H = len(img[:,0,0])
    W = len(img[0,:,0])
    
    #initial start positions 
    cell_start_x = 0
    cell_start_y = 0
    
    #on grid of small images inside the crop buffer of the large images
    on_grid = True
    
    #scan over large image to get small ones
    while on_grid == True :
        cell_end_x = cell_start_x + w 
        cell_end_y = cell_start_y + h
       # print(cell_end_x, cell_end_y, cell_start_x, cell_start_y)
        cropped = img[cell_start_x:cell_end_x, cell_start_y:cell_end_y, :]
        #print(cropped.shape)
        obj_num += 1
        
        new_img = Image.fromarray(cropped)
        if len(cropped[:,0])==416 and len(cropped[0,:])==416 :
            print(len(cropped[:,0]), len(cropped[0,:]))
            new_img.save(f"{mypath}{dir_name}/{obj_num}.png")

        if (cell_start_y + 1.5*w > W) :
            on_grid = False
        elif cell_start_x + 1.5*h < H :
            cell_start_x += (h + np.random.randint(cell_margin) )
        else :
            cell_start_x = np.random.randint(cell_margin)
            cell_start_y += (w + np.random.randint(cell_margin))

            
 
