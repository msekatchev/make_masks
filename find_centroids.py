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
    #cv2.imwrite("pmts_gray--4.png",pmts_gray)
    #cv2.imwrite("bolts_gray--4.png",bolts_gray)
    #cv2.imwrite("img--4.png",img)





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
        pmtID = input("Input PMT number:\n-->")
        #Draw hough circles on img
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        cv2.circle(img,(i[0],i[1]),2,(0,255,0),3)

        #draw bolt locations and number them 
        bolt_no = 0
        #print("I is ",i)
        cv2.putText(img, pmtID, (i[0]-47, i[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 1)
        
        ######################### Automatic bolt number labelling on mask ##############################
        radius = i[2]
        for j in bolts_ord :
            bolt_no += 1
            
            #Find the angle at the centre of the PMT between the x axis and 
            #the line pointing from the centre of the PMT to the centre of the bolt
            lengthx = j[1]-i[0]
            lengthy = j[0]-i[1]
            length = math.sqrt(lengthx**2+lengthy**2)
            if(lengthx==0):
                angle=3.1415926/2
            else:
                angle = np.arctan(lengthy/lengthx)
            
            #Calculate text location based on this angle and the location of the bolt along the circle.
            
            #bolt 1
            if(bolt_no==1):
                textx = int(j[1])
                texty = int(j[0]-(32))
            #bolts 2 through 14 (on the right side of the circle/the 1st and 4th quadrant) 
            elif(bolt_no<=12):
                textx = int(j[1]+(28)*np.cos(angle))
                texty = int(j[0]+(28)*np.sin(angle))
            #bolt 13
            elif(bolt_no==13):
                textx = int(j[1]+abs((34)*np.cos(angle)))
                texty = int(j[0]+abs((34)*np.sin(angle)))
            #bolts 14 through 19 (on the 3rd quadrant)
            elif(bolt_no<=19):
                textx = int(j[1]-(40)*np.cos(angle))
                texty = int(j[0]-(40)*np.sin(angle))
            #bolts 20 through 24 (on the 2nd quadrant)
            else:
                textx = int(j[1]-(37)*np.cos(angle))
                texty = int(j[0]-(37)*np.sin(angle))
            pointerx = int((textx+textx+20)/2)
            pointery = int((texty+texty-20)/2)
            cv2.line(img, (j[1],j[0]), (pointerx,pointery), (0,177,177), thickness=1, lineType=8, shift=0)

            cv2.rectangle(img,(textx,texty),(textx+15,texty-15),(0,0,0), thickness=-1, lineType=8, shift=0)
            #cv2.circle(img,(textx,texty),10,(0,0,0),-1)
            cv2.circle(img, (j[1], j[0]), 5, (0,0,255), -1)
            cv2.putText(img, f'{bolt_no}', (textx, texty), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,255), 1)
        ######################### Automatic bolt number labelling on mask ##############################
            

    #draw bolt locations


        #for i in bolts_ord :
            print(j[0],j[1])
            
        

    print(circles)
    print("SAVING")

    base = os.path.basename(img_path)
    filename = os.path.splitext(base)[0]
    outputMaskName = os.path.join(filename+'-labelled.png')
    print("Saving labelled output mask to: ",outputMaskName)
    #save output mask in code directory
    cv2.imwrite(outputMaskName, img)
