import cv2
import numpy as np
from skimage import color, img_as_ubyte
import os, sys
import math
#find_centroids("B.png")

def find_centroids(img_path) :

    img = cv2.imread(img_path)

    train_labels = img

    lower_pmts = np.array([1, 1, 1], dtype = "uint16")
    upper_pmts = np.array([1,1,1], dtype = "uint16")
    lower_bolts = np.array([2, 2, 2], dtype = "uint16")
    upper_bolts = np.array([2,2,2], dtype = "uint16")

    pmts_gray = cv2.inRange(train_labels, lower_pmts, upper_pmts)
    bolts_gray = cv2.inRange(train_labels, lower_bolts, upper_bolts)
    img = cv2.cvtColor(bolts_gray,cv2.COLOR_GRAY2BGR)
    cv2.imwrite("pmts_gray--4.png",pmts_gray)
    cv2.imwrite("bolts_gray--4.png",bolts_gray)
    cv2.imwrite("img--4.png",img)








    #print('images made')

    #Calls HoughCircles() to find multiple PMTs in an image

    #Outpts list of circle parameters
    ################################################################
    def find_pmts(gray_img) :
        out = []
        edges = cv2.Canny(gray_img,0,100)
        circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,dp=1,
                               minDist=200,
                               param1=100,
                               param2=20,
                               minRadius=100,
                                maxRadius=200
                              )
        #print(circles)

        ##Error over here vvvv, because circles is empty.
        circles = np.uint16(np.around(circles))
        img2 = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)


        return circles
    ################################################################




    ################################################################

    #Find centroids of bolts near edge of circles in find_pmts() using findContours()

    #Output is a list of bolt locations for a given circle 
    def ret_centres(image, params) :
        out = []
        x = params[1]
        y = params[0]
        r = params[2]
        L = int(r*1.5)
        gray_image = image[x-L:x+L, y-L:y+L]
        ret,thresh = cv2.threshold(gray_image,127,255,0)
        gray_image = color.gray2rgb(img_as_ubyte(gray_image))

    # find contours in the binary image
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        #Loop over bolts and find centroid
        for c in contours:
        #moments
            M = cv2.moments(c)
            area = cv2.contourArea(c)
        
            if (area <=20) or (area>= 1000) :  # skip ellipses smaller then 10x10
                continue
            
           # calculate x,y coordinate of center, breaks if m00 = 0 output location in large image (offset)
            elif M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                out.append([cY + (x-L), cX + (y-L)])
             #   print(area)

            else:
                continue
        return out
    ################################################################
    
    
    
    
    ################################################################
    # From a list of bolt positions and circle parameters, orders bolts in clockwise order starting from top over 360 degrees
    
    #returns a list of bolts in clockwise order 
    def order_bolts(circle, bolt_ring) :
        out = []
        
        #circle parameters
        circ_x = circle[0]
        circ_y = circle[1]
        circ_r = circle[2]
        L = int(circ_r*1)  
        
        #bolt locations found beforehand
        nodes = np.asarray(bolt_ring)
        
        #loop over 2pi in (60 for now) steps finding closest bolts
        for i in np.linspace(0, 2*3.14159, num=60) : 
            
            #point on circle (scaled by radius of hough transform) to search near
            search_x = int(circ_x + L*np.sin(i))
            search_y = int(circ_y - L*np.cos(i))
            
            #find bolt closest to point
            dist = np.sum((nodes - [search_y,search_x])**2, axis=1)
            closest = np.argmin(dist)
            
            #only append each bolt coordinate once
            if bolt_ring[closest] not in out :
                out.append(bolt_ring[closest])
               
        return out
    
    ################################################################




    #find circles in image
    circles = find_pmts(pmts_gray)


    #loop over circles and find bolts, end up with list of circles, each a list of bolts (no circle parameters are saved )
    for i in circles[0, :] :
        bolt_ring = ret_centres(bolts_gray, i)
        bolts_ord = order_bolts(i, bolt_ring)

        #Draw hough circles on img
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        cv2.circle(img,(i[0],i[1]),2,(0,255,0),3)

        #draw bolt locations and number them 
        bolt_no = 0
        #print("I is ",i)
        for j in bolts_ord :
            bolt_no += 1
            lengthx = j[1]-i[0]
            lengthy = j[0]-i[1]
            length = math.sqrt(lengthx**2+lengthy**2)
            angle = np.arctan(lengthy/lengthx)
            
            if(bolt_no==1):
                textx = int(j[1])
                texty = int(j[0]-40)
            elif(bolt_no<=13):
                textx = int(j[1]+35*np.cos(angle))
                texty = int(j[0]+35*np.sin(angle))
            elif(bolt_no<=19):
                textx = int(j[1]-60*np.cos(angle))
                texty = int(j[0]-60*np.sin(angle))
            else:
                textx = int(j[1]-50*np.cos(angle))
                texty = int(j[0]-50*np.sin(angle))
            cv2.line(img, (textx, texty), (j[1],j[0]), (0,255,255), thickness=1, lineType=8, shift=0)
            cv2.putText(img, f'{bolt_no}', (textx, texty), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,0,255), 1)
            
 
    #draw bolt locations


    for i in bolts_ord :
        print(i[0],i[1])
        #for j in i :
        cv2.circle(img, (i[1], i[0]), 5, (0,0,255), -1)
            #print(j)

    print(circles)
    print("SAVING")
    cv2.imwrite('out.png', img )
