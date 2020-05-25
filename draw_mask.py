 
import cv2
import os
import numpy as np

global drawing, rdrawing, img

#TODO: undo button?
#TODO: name window

####annotate_dir("images/datasets/bolts", "_dyn", "train", 5, 10)
####annotate_img("test/142.png",150,7)
#Set up callbacks for drawing circles on click and drag, bound to left and middle mouse 
def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    global ix, iy, drawing, rdrawing, mode
    #Left click blue
    if event == cv2.EVENT_LBUTTONDOWN and (flags == cv2.EVENT_FLAG_LBUTTON):
        drawing = True
        ix,iy = x,y
        cv2.circle(img, (x, y), large_size,(255,0,0),-1)

    elif event == cv2.EVENT_MOUSEMOVE and (flags == cv2.EVENT_FLAG_LBUTTON):
        if drawing == True:
                cv2.circle(img, (x, y), large_size,(255,0,0),-1)
    elif event == cv2.EVENT_LBUTTONUP and (flags == cv2.EVENT_FLAG_LBUTTON):
        drawing = False
    
    #Middle click blue
    if event == cv2.EVENT_MBUTTONDOWN and (flags == cv2.EVENT_FLAG_MBUTTON):
        rdrawing = True
        ix,iy = x,y
        cv2.circle(img, (x, y), small_size,(255,0,0),-1)

    elif event == cv2.EVENT_MOUSEMOVE and (flags == cv2.EVENT_FLAG_MBUTTON):
        if rdrawing == True:
                cv2.circle(img, (x, y), small_size,(255,0,0),-1)
    elif event == cv2.EVENT_MBUTTONUP and (flags == cv2.EVENT_FLAG_MBUTTON):
        rdrawing = False
        
        
    #left click red
    if event == cv2.EVENT_LBUTTONDOWN and (flags & cv2.EVENT_FLAG_SHIFTKEY):
        drawing = True
        ix,iy = x,y
        cv2.circle(img, (x, y), 7,(0,0,255),-1)

    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_SHIFTKEY):
        if drawing == True:
                cv2.circle(img, (x, y), 7,(0,0,255),-1)
    elif event == cv2.EVENT_LBUTTONUP and (flags & cv2.EVENT_FLAG_SHIFTKEY):
        drawing = False
    
        

#Set up for a single image 
def annotate_img(img_path, size1, size2) :
    #Create window and put it in top left corner off screen
    cv2.namedWindow('image')
    cv2.moveWindow('image', 40, 30)
    global drawing, rdrawing, large_size, small_size, img
    large_size=size1
    small_size=size2
    
    img = cv2.imread(img_path)
    cv2.setMouseCallback('image',draw_circle)

    #Drawing and keyboard callbacks a to skip and delete, s to save image
    drawing = False
    rdrawing = False
    while(1):
        cv2.imshow('image',img)
        k = cv2.waitKey(20) & 0xFF
        if k == ord('s'):
            #cv2.destroyWindow('image')
            break

    #Make mask same colour as drawing and output binarised image
    train_labels = img[:,:,:3]
    lower_blue = np.array([254,0,0], dtype = "uint16")
    upper_blue = np.array([255,0,0], dtype = "uint16")
    mask_blue = cv2.inRange(train_labels, lower_blue, upper_blue)
    mask_blue[mask_blue < 250] = 0
    #mask_blue[mask_blue != 0 ] = 255
    mask_blue[mask_blue != 0 ] = 1

##NEW
    lower_red = np.array([0,0,254], dtype = "uint16")
    upper_red = np.array([0,0,255], dtype = "uint16")
    mask_red = cv2.inRange(train_labels, lower_red, upper_red)
    mask_red[mask_red < 250] = 0
    #mask_red[mask_red != 0 ] = 255  
    mask_red[mask_red != 0 ] = 2
    #Add the masks together to get array of pixel labels
    mask = np.add(mask_red, mask_blue)
    #mask = cv2.bitwise_or(mask_red,mask_blue)
    print(np.unique(mask))
 ##eND NEW

    #save label in code directory
    cv2.imwrite('label.png', mask)
    cv2.imwrite('labelred.png', mask_red)
    cv2.imwrite('labelblue.png',mask_blue)
    print(mask_red)
    cv2.destroyWindow('image')
    return
            

#Set up for directory of images with file structure for image segmentation
def annotate_dir(img_dir, dataset, subset, size1, size2) :
    #Create window and put it in top left corner off screen
    cv2.namedWindow('image')
    cv2.moveWindow('image', 40, 30)
    global drawing, rdrawing, large_size, small_size, img
    large_size=size1
    small_size=size2

    
    cv2.setMouseCallback('image',draw_circle)
    #Array of names in directory to iterate over
    f = []
    for (dirpath, dirnames, filenames) in os.walk(f'{img_dir}{dataset}/{subset}_frames/{subset}'):
        f.extend(filenames)
        break
    
    #print(f)
    
    for i in f :
        skip = False
        drawing = False
        rdrawing = False
        img = cv2.imread(f'{img_dir}{dataset}/{subset}_frames/{subset}/{str(i)}')
        
        #Drawing and keyboard callbacks a to skip and delete, s to save image
        while(1):
            cv2.imshow('image',img)
            k = cv2.waitKey(20) & 0xFF
            if k == ord('s'):
                #cv2.destroyWindow('image')
                break
            elif k == ord('a'):
                skip = True
                #cv2.destroyWindow('image')
                break
            elif k == ord('r'):
                img = cv2.imread(f'{img_dir}{dataset}/{subset}_frames/{subset}/{str(i)}')
                #cv2.destroyWindow('image')
        #Make mask y selecting same colour as drawing and output binarised image
        train_labels = img[:,:,:3]
        lower_blue = np.array([254,0,0], dtype = "uint16")
        upper_blue = np.array([255,0,0], dtype = "uint16")
        mask_blue = cv2.inRange(train_labels, lower_blue, upper_blue)
        mask_blue[mask_blue < 250] = 0
        #mask_blue[mask_blue != 0 ] = 255
        mask_blue[mask_blue != 0 ] = 1
        
        lower_red = np.array([0,0,254], dtype = "uint16")
        upper_red = np.array([0,0,255], dtype = "uint16")
        mask_red = cv2.inRange(train_labels, lower_red, upper_red)
        mask_red[mask_red < 250] = 0
        #mask_red[mask_red != 0 ] = 255  
        mask_red[mask_red != 0 ] = 2

        #Add the masks together to get array of pixel labels
        mask = np.add(mask_red, mask_blue)
        print(np.unique(mask))
        
        #Save label or delete image
        if skip == False :
            cv2.imwrite(f'{img_dir}{dataset}/{subset}_masks/{subset}/{str(i)}', mask)
        else :
            os.remove(f'{img_dir}{dataset}/{subset}_frames/{subset}/{str(i)}')
    cv2.destroyWindow('image')
