#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 00:33:33 2018

@author: hanihussein
"""
from pyzbar import pyzbar
import cv2   
import numpy as np   #import numpy library for arrays usages
import urllib.request
import time


def read_usb(i):
    cv2.namedWindow('QR-code',cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow('QR-code', 400,400)

    timeout = time.time() + 10  
    capture = cv2.VideoCapture(i)
    while True:
        ret, img = capture.read()
        
        cv2.imshow("QR-code", img)

        barcodes = pyzbar.decode(img)
        
        if(len(barcodes)>0):
            cv2.destroyAllWindows()
            return barcodes[0].data, False
        
        if time.time() > timeout:
            print("Getting QR time out .. exit")
            cv2.destroyAllWindows()
            return None, True
        
        #wait for key pressed
        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop (Exit)
        if key == ord("q"):
            break


def read_once(url):
    #start the process loop
    while True:

        imgResp=urllib.request.urlopen(url)
        imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
        img=cv2.imdecode(imgNp,-1)
        
        barcodes = pyzbar.decode(img)
        
        print(len(barcodes))
        for i,barcode in enumerate(barcodes):
            print(i," >>> ",barcode.data) #Print only the "data" of the QR-Code
        
        
        
        #wait for key pressed
        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop (Exit)
        if key == ord("q"):
            break

def read_multiple(url):
    #start the process loop
    while True:

        imgResp=urllib.request.urlopen(url)
        imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
        img=cv2.imdecode(imgNp,-1)
        
        barcodes = pyzbar.decode(img)
        
        print(len(barcodes))
        for i,barcode in enumerate(barcodes):
            print(i," >>> ",barcode.data) #Print only the "data" of the QR-Code
        
        
        
        #wait for key pressed
        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop (Exit)
        if key == ord("q"):
            break


#read_usb(2)