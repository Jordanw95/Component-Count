from tkinter.filedialog import askopenfilename
import cv2
from pubsub import pub
import PIL.ImageTk, PIL.Image
import numpy as numpy
import sqlite3


class Model :
    def __init__(self) : 
        # Flag to ensue image has been loaded
        self.flagLoadImage = False

        return 

    def loadImg(self): 
        # Pop up image
        print("Model receieved")
        path = askopenfilename(initialdir = "./", 
            filetypes = [("bmp files", "*.bmp"),  ("All Files", "*.*")],
            title = "Choose a file."
            )
        if len(path) > 0 : #Check for picking result
            self.greyOrigImg = cv2.imread(path, 0)
            self.originalImg = cv2.imread(path)  #Saving original image to use later
            self.currentImg = self.originalImg.copy() 
            pub.sendMessage("model_updated", data  = self.toTkImg(self.currentImg))  #Converts image to format that can be displayed in TK widget. (could this slow things down?)
            print("Model gets here")
            self.flagLoadImage = True
            self.find_average(200, 1000)
    def toTkImg(self, img) : 
        """There may be better ways to do this for monochrome images later on (see bear notes)"""
        #cv2 image is in bgr format 
        b, g, r = cv2.split(img)
        # merge into one dimension array in rgb sequence
        img = cv2.merge((r, g, b))
        #Need to resize image for display
        img = self.resize_img(img)
        # convert rgb  array into 2 dim PIL image array
        im = PIL.Image.fromarray(img)
        # convert PIL array into tkinter image
        imgtk = PIL.ImageTk.PhotoImage(image = im)
        return imgtk
    
    def resize_img(self, frame) :
        return cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)))
    
    def binarise_img(self, val):
        if self.flagLoadImage :
            img = self.originalImg.copy()
            bin_img = cv2.threshold(img, val, 255, cv2.THRESH_BINARY)[1]
           
            #Binarise image and put it into current image
            self.currentImg = bin_img 
            pub.sendMessage("model_updated", data = self.toTkImg(self.currentImg))
            
    def original_img(self) : 
        if self.flagLoadImage :
            pub.sendMessage("model_updated", data = self.toTkImg(self.originalImg))

    def find_average(self, val, minvalue) : 
        if self.flagLoadImage :
            img = self.greyOrigImg.copy()
            org_binarised_img = cv2.threshold(img, val, 255, cv2.THRESH_BINARY)[1]
            contours_img = cv2.bitwise_not(org_binarised_img)
            _,cnts,hierarchy = cv2.findContours(contours_img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


            cnts_areas = [cv2.contourArea(x) for x in cnts]
            cnts_areas = [x for x in cnts_areas if x > minvalue]
            self.current_avg = (sum(cnts_areas)) / (len(cnts_areas))
            pub.sendMessage("average_value", data = self.current_avg)

            if cnts_areas : 
                detectedParts = len(cnts_areas)
                maxDiff = (max(cnts_areas)) - (min(cnts_areas))
                pub.sendMessage("setting_check", data = [detectedParts, maxDiff])
            else :
                pub.sendMessage("setting_check", data = [0, 0])


            

    
    

class DataStore :
    
    def __init__(self):
        self.conn = sqlite3.connect('PartCountData')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS imginfo (id integer PRIMARY KEY, partnumber TEXT, barcode TEXT, average TEXT, binaryvalue TEXT, minvalue TEXT)")
        self.conn.commit()
    
    def add_entry(self, partnumber, barcode, average, binaryvalue, minvalue) :
        self.cur.execute("INSERT INTO imginfo VALUES (NULL, ?, ?, ?, ?, ?)", (partnumber, barcode, average, binaryvalue, minvalue))
        self.conn.commit()

    def view_all(self):
        self.cur.execute("SELECT * FROM imginfo")
        rows = self.cur.fetchall()
        print(rows)

    def __del__(self):
        self.conn.close()

