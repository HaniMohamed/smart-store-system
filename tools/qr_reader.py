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

def read_usb(i):
    capture = cv2.VideoCapture(i)
    while True:
        ret, img = capture.read()
        
        cv2.imshow("image ", img)

        barcodes = pyzbar.decode(img)
        
        if(len(barcodes)>0):
            return barcode.data
            break
        
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