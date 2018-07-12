
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 21:51:01 2017

@author: hanihussein
"""

import cv2   #import openCV library for the computer vision
import numpy as np   #import numpy library for arrays usages
import urllib.request



def detect_objects(url):
    yellow = [(20, 100, 100),(30, 255, 255)] 
    green = [(33,60,40),(102,255,255)]

    objColors=[yellow, green]

    kernelOpen = np.ones((20, 20))    #Max. array of pixels that cosider as noise pixels  -> look at [2]
    kernelClose = np.ones((2, 2)) #array of pixels which will fill in -> look at [3]

    #start the process loop
    while(True):
        yellowObj = 0
        greenObj = 0

        imgResp=urllib.request.urlopen(url)
        imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
        img=cv2.imdecode(imgNp,-1)

        img = cv2.resize(img,(340,220)) #resize img window
        height, width = img.shape[:2] #get width and height of the frame
        #draw the center of the frame
        cv2.rectangle(img, (int(width/2),int(height/2)), (int(width/2),int(height/2)),(255,0,0), 5)

        #Convert BGR color to HSV
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        for i, (lowerBound, upperBound) in enumerate(objColors):
            #Create Mask, Showing only rquired color using the HSV range of the color
            mask = cv2.inRange(imgHSV,lowerBound, upperBound)   # -> [1]

            #Clear noise pixels
            maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen) # -> [2]
                        
            #Fill in the object tracked
            maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose) # -> [3]
            
            finalMask = maskClose #define the final mask to work on
            
            #Get the contour of the object
            _, conts, _ = cv2.findContours(finalMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
            if i==0:
                #print("yellow",">>>>",len(conts))
                yellowObj = len(conts)
                cv2.imshow("yellowMask", maskClose) 
            elif i==1:
                #print("green",">>>>",len(conts))
                greenObj = len(conts)
                cv2.imshow("greenMask", maskClose) 

        return greenObj, yellowObj

        #Showing Camera frame
        cv2.imshow("Camera", cv2.flip( img, 1 )) 

        #wait for key pressed
        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop (Exit)
        if key == ord("q"):
            break

    cv2.destroyAllWindows()

