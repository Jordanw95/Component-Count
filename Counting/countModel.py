import os 

os.environ["PYLON_CAMEMU"] = "3"

from tkinter.filedialog import askopenfilename
import cv2
from pubsub import pub
import PIL.ImageTk, PIL.Image
import numpy as numpy
import sqlite3
from pypylon import genicam
from pypylon import pylon
import sys
import time



class Model :


    def counting_frame(self, frame, average, binaryvalue, minvalue) :
        if average :
            cframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.smart_count(cframe, average, binaryvalue, minvalue)
            if self.check :
                self.check1 = False
            pub.sendMessage("Severe_Overlap", data = self.check1)
            if self.check1 : 
                new_frame = self.draw_overlap(frame, self.index_of_overlap, self.cnts)
                return new_frame
            else:
                return frame
            
                # Return modified frame else return normal frame

    def draw_overlap (self, frame, index_of_overlap, cnts) :
        self.index_of_overlap = list(set(self.index_of_overlap))
        cnts_draw = [cnts[x] for x in self.index_of_overlap]
        to_draw = []
        for c in cnts_draw : 
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 4)
        return frame



    def smart_count(self,Cframe, average, binaryvalue, minvalue) : 
        img = Cframe
        org_binarised_img = cv2.threshold(img, binaryvalue, 255, cv2.THRESH_BINARY)[1]
        contours_img = cv2.bitwise_not(org_binarised_img)

        _,cnts,hierarchy = cv2.findContours(contours_img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        self.cnts = cnts

        cnts_areas = [cv2.contourArea(x) for x in cnts]
        cnts_areas = list(enumerate(cnts_areas))        
        cnts_areas = [x for x in cnts_areas if x[1] > minvalue]

        self.final_count= 0
        self.blob_sizes = []

        for blob in cnts_areas : 
            count = round(blob[1]/average)
            self.final_count += count
            self.blob_sizes.append((blob[0], count))

        self.severe_overlap(average, cnts_areas, self.blob_sizes)
        self.incorrect_program(average, cnts_areas)

        pub.sendMessage("Count_Updated", data = self.final_count)

    
    def severe_overlap(self, average, cnts_areas, blob_sizes) : 
        self.check1 = False
        overlap = 0
        index_of_overlap = []
        for blob in cnts_areas : 
            diff = abs((blob[1]/average) - round(blob[1]/average))
            if diff > 0.25 : 
                overlap += 1
                index_of_overlap.append(blob[0])

        if overlap > 0 :
            self.check1 = True

        for counts in blob_sizes : 
            if counts[1] > 4 :
                self.check1 = True
                index_of_overlap.append(counts[0])
        if self.check1 :
            self.index_of_overlap = index_of_overlap





    def incorrect_program (self, average, cnts_areas) :
        self.check = False
        if cnts_areas :
            pure_cnts_areas = [x[1] for x in cnts_areas]
            if  min(pure_cnts_areas) > (average *1.3 ):
                self.check = True
            if min(pure_cnts_areas) < (average *0.7) :
                self.check = True
        pub.sendMessage("incorrect_program", data = self.check)




        
    
    
    

class DataStore :
    
    def __init__(self):
        self.conn = sqlite3.connect('PartCountData')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS imginfo (id integer PRIMARY KEY, partnumber TEXT, barcode TEXT, average TEXT, binaryvalue TEXT, minvalue TEXT)")
        self.conn.commit()
        self.conn.close()
    
    def add_entry(self, partnumber, barcode, average, binaryvalue, minvalue) :
        self.conn = sqlite3.connect('PartCountData')
        self.cur = self.conn.cursor()
        self.cur.execute("INSERT INTO imginfo VALUES (NULL, ?, ?, ?, ?, ?)", (partnumber, barcode, average, binaryvalue, minvalue))
        self.conn.commit()
        self.conn.close()

    def view_all(self):
        self.conn = sqlite3.connect('PartCountData')
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM imginfo")
        rows = self.cur.fetchall()
        print(rows)
        self.conn.commit()
        self.conn.close()

    def search_entry (self, partnumber = "", barcode = "") :
        self.conn = sqlite3.connect('PartCountData')
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM imginfo WHERE partnumber = ? OR barcode = ?", (partnumber, barcode))
        rows = self.cur.fetchall() 
        self.conn.commit()
        self.conn.close()
        return rows

    # def __del__(self):
    #     self.conn.close()

    
class CameraCapture :
    def __init__(self):
        self.img0 = []
        self.windowName = 'title'
        self.model = Model()

        # try:
        # Create an instant camera object with the camera device found first.
        print('a')
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        print('b')            
        self.camera.Open()  
        print('c')
        # According to their default configuration, the cameras are
        # set up for free-running continuous acquisition.
        #Grabbing continuously (video) with minimal delay
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        print('d')
        # converting to opencv bgr format
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned


    def getFrame(self):
        try:
            self.grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if self.grabResult.GrabSucceeded():
                image = self.converter.Convert(self.grabResult) # Access the openCV image data
                self.img0 = image.GetArray()


            else:
                print("Error: ", self.grabResult.ErrorCode)
    
            self.grabResult.Release()
            #time.sleep(0.01)

            return self.img0
            
        except genicam.GenericException as e:
            # Error handling
            print("An exception occurred.", e.GetDescription())
            exitCode = 1

