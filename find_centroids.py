import cv2
import numpy as np
from skimage import color, img_as_ubyte
import os, sys
###find_centroids("images/datasets/bolts_dyn/test_frames/test/90.png")
###find_centroids("test/label6.png")
###find_centroids("B.png")
#### testcode("test/label6.png")
def testcode(img_path):

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



def find_centroids(img_path) :
    img = cv2.imread(img_path)

    #Set up separate masks for bolts and pmts and an output image
    #train_labels = img
    #lower_pmts = np.array([254, 0, 0], dtype = "uint16")
    #upper_pmts = np.array([255,0,0], dtype = "uint16")
    #lower_bolts = np.array([0, 0, 254], dtype = "uint16")
    #upper_bolts = np.array([0,0,255], dtype = "uint16")

    #pmts_gray = cv2.inRange(train_labels, lower_pmts, upper_pmts)
    #bolts_gray = cv2.inRange(train_labels, lower_bolts, upper_bolts)
    #img = cv2.cvtColor(bolts_gray,cv2.COLOR_GRAY2BGR)

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
        #127
        cv2.imwrite("gray_image.png",gray_image)
        ret,thresh = cv2.threshold(gray_image,127,255,0)
        gray_image = color.gray2rgb(img_as_ubyte(gray_image))
        ###find_centroids("B.png")
        cv2.imwrite("threshold1.png",thresh)
        # find contours in the binary image
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #print(contours)
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
                out.append([cX + (y-L),cY + (x-L)])
                #print(area)

            else:
                continue
        k=0
        while(k<len(out)):
            print(str(k+1)+" - X:"+str(out[k][0])+" Y:"+str(out[k][1]))
            
            k=k+1
            
        return out
    ################################################################





    #find circles in image
    circles = find_pmts(pmts_gray)
    #print(circles)
    bolt_centres = []

    #loop over circles and find bolts, end up with list of circles, each a list of bolts (no circle parameters are saved )
    for i in circles[0, :] :
        bolt_ring = ret_centres(bolts_gray, i)
        #print("i = ",i)
        bolt_centres.append(bolt_ring)
    
        #Draw hough circles on img
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        cv2.circle(img,(i[0],i[1]),2,(0,255,0),3)


    #draw bolt locations
    for i in bolt_centres :
        for j in i :
            cv2.circle(img, (j[0], j[1]), 5, (0,0,255), -1)

    #print(bolt_ring)
    #print(bolt_centres)
    #print(circles)
    print("SAVING")
    cv2.imwrite('out.png', img )
 
