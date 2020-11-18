from countView import View
from countModel import Model, DataStore, CameraCapture
from tkinter import *
from pubsub import pub
import time
import cv2

class Controller :
    def __init__(self, parent): #Parent is the tkinter main window
        #variables
        self.parent = parent
        self.model = Model() #point to model object
        # self.model.get_data(False, False)
        self.datastore = DataStore()
        self.current_prog = False
        self.view = View(parent)
        self.view.setup()
        self.cam = CameraCapture()
        self.programLoadFlag = None
        self.delay = 90
        self.update()

        



        pub.subscribe(self.loadProg_btn_pressed, "Find_Prog_Button_pressed")
        pub.subscribe(self.saveImg_btn_pressed, "Save_Img_Button_Pressed")


        # This will hadle all situation when Model has been changed to refresh View or values
        pub.subscribe(self.model_change_handler, "model_updated")
        pub.subscribe(self.count_update_handler, "Count_Updated")
        pub.subscribe(self.severe_overlap_handler, "Severe_Overlap")
        pub.subscribe(self.incorrect_program_handler, "incorrect_program")
 

    def update(self):
        
        self.severe_overlap = False
        frame = self.cam.getFrame()
        if self.current_prog : 
            frame = self.model.counting_frame(frame, float(self.current_prog[0][3]), float(self.current_prog[0][4]), float(self.current_prog[0][5]))
            #if severeoverap here modify frame too draw it?



        frame = cv2.resize(frame, dsize = (1000,600), interpolation = cv2.INTER_CUBIC)
        self.view.updateCanvas(frame)
        self.parent.after(self.delay, self.update)

       

    def model_change_handler(self, data) : 
        self.view.updateImg(data)


    def count_update_handler(self, data) : 
        self.view.count_update(data)

    def average_value_update(self, data) :
        self.view.updateAverage(data)
    
    def saveImg_btn_pressed(self) : 
        frame = self.cam.getFrame()

        cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".bmp",
                    cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))        

    def loadProg_btn_pressed(self) :
        progref = [self.view.partnum_entry.get(), self.view.barcode_entry.get()]
        if progref.count("") > 1 :
            self.view.prog_label_update("Please enter barcode or partnumber")
        else :
            self.current_prog = self.datastore.search_entry(self.view.partnum_entry.get(), self.view.barcode_entry.get())
            if self.current_prog :
                self.view.current_label_update(f"Current Program : {self.current_prog[0][1]}")
            else :
                self.view.prog_label_update("Invalid barcode or partnumber please try again")
    
    def severe_overlap_handler(self, data) : 
        print("receiving")
        if data : 
            self.view.severe_overlap_update("Severe Overlap", "red")
        else : 
            print("data sent must be wrong")
            self.view.severe_overlap_update("", "white")

    def incorrect_program_handler(self, data) : 
        if data : 
            self.view.incorrect_program_update("Incorrect Program or Poor Presentation", "red")
        else :
            self.view.incorrect_program_update("", "white")
       
        



#application entry point main method
    #create instance of tk
if __name__ == "__main__":
    mainwin = Tk()

    mainwin.geometry("1400x1200")
    mainwin.title("PartCounting")
    app = Controller(mainwin)
    mainwin.mainloop()