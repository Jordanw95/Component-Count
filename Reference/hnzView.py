import tkinter as tk
from tkinter import *
from pubsub import pub

class View : 
    def __init__(self, parent) :
        # initize variables
        self.container = parent
        return

    def setup(self):
        self.create_widgets()
        self.setup_layout()
        
    def create_widgets(self) :
        """Create various widgets in the tkinter main window"""
        # set up frame
        self.topFrame = Frame(self.container, borderwidth =2, highlightbackground = "black",
            highlightcolor = "red", highlightthickness = 1, width = 300, height = 600)
        self.bottomFrame = Frame(self.container, borderwidth =2, highlightbackground = "black",
            highlightcolor = "red", highlightthickness = 1, width = 700, height = 700)
        self.rightFrame = Frame(self.container, borderwidth =2, highlightbackground = "black",
            highlightcolor = "red", highlightthickness = 1, width = 500, height = 600)
        self.topFrame2 = Frame(self.topFrame)
        self.topRight = Frame(self.topFrame)
        # button
        self.b1LoadImg = tk.Button(self.topFrame2, text = "Load Image", command = self.loadImg)
        self.b2Orig = tk.Button(self.topFrame2, text = "Original Image", command = self.OriginalImg)
        # scale bars
        self.scale1 = tk.Scale(self.topFrame, from_ = 0, to = 255, orient= HORIZONTAL, length= 500,  label = 'Binary Threshold',
            command = self.scalarChangeBin )
        
        self.scale2 = tk.Scale(self.topFrame, from_ = 200, to = 5000, orient= HORIZONTAL, length= 500,  label = 'Minimum Detectable Object',
            command = self.scalarChangeMin )

        self.scale1.set(200)
        self.scale2.set(1000)
        # image panel
        self.panelA = tk.Label(self.bottomFrame, pady = 50)

        self.partcount_label = tk.Label(self.topRight, text = "Number parts detected :", width = 20, anchor=W , justify=LEFT)
        self.partcount_val = tk.Label(self.topRight, text = "", anchor=W, justify=RIGHT )

        self.diff_label = tk.Label(self.topRight, text = "Max difference between parts :", width = 20, anchor=W , justify=LEFT)
        self.diff_val = tk.Label(self.topRight, text = "", anchor=W, justify=RIGHT )

        self.binary_label = tk.Label(self.rightFrame, text = "Binary Threshold :", width = 20, anchor=W , justify=LEFT)
        self.binary_val = tk.Label(self.rightFrame, text = "", anchor=W, justify=RIGHT )

        self.min_label = tk.Label(self.rightFrame, text = "Minimum Detectable Object :", width = 20, anchor=W , justify=LEFT)
        self.min_val = tk.Label(self.rightFrame, text = "", anchor=W, justify=RIGHT )

        self.avg_label = tk.Label (self.rightFrame, text = "Average :", width = 20, anchor=W , justify=LEFT)
        self.avg_val = tk.Label (self.rightFrame, text = "")

        self.partnum_label = tk.Label (self.rightFrame, text = "Enter Part number: ", width = 20, anchor=W , justify=LEFT)
        self.partnum_entry = tk.Entry(self.rightFrame)

        self.barcode_label = tk.Label (self.rightFrame, text = "Enter barcode number: ", width = 20, anchor=W , justify=LEFT)
        self.barcode_entry = tk.Entry(self.rightFrame)

        self.save_button = tk.Button (self.rightFrame, text = "Save Reference", command = self.saveRef)
        self.save_warning = tk.Label(self.rightFrame, text = "")


    def loadImg(self) :
        print("loading")
        pub.sendMessage("OpenFile_Button_Pressed") #sending message from gui
    
    def OriginalImg(self) :
        print("OriginalImg")
        pub.sendMessage("OriginalImg_Button_Pressed")

    def scalarChangeBin(self, val) :
        self.binary_val["text"]=[f"{val}"]
        pub.sendMessage("ScalarBinChange_Button_Pressed")

    def scalarChangeMin(self, val) :
        self.min_val["text"]=[f"{val}"]
        pub.sendMessage("ScalarMinChange_Button_Pressed")

    def updateImg(self, img):
        self.panelA.configure(image = img)
        self.panelA.image=img
        return

    def saveRef(self) : 
        self.save_warning["text"]=[""]
        pub.sendMessage("SaveRef_Button_Pressed")

    def savemissingfields(self):
        self.save_warning["text"]=["Please fill in all fields above"]


    def updateAverage (self, data): 
        self.avg_val["text"] = ["%.2f" % data]
    
    def set_check_update (self, data) : 
        self.partcount_val["text"] = ["%.2f" % data[0]]
        self.diff_val["text"] = ["%.2f" % data[1]]



    def setup_layout(self) : 
        # pack top and bottom frames
        self.topFrame.pack(side= TOP)
        self.bottomFrame.pack(side = LEFT, padx = 25, pady = 25)
        self.rightFrame.pack(side = RIGHT, padx = 25, pady = 25)
        # pack top2 inside of top frame
        self.topFrame2.pack(side = TOP)
        self.topRight.pack(side = RIGHT, padx = 20)
        # Pack 2 buttons to top frame
        self.b1LoadImg.pack(side = LEFT)
        self.b2Orig.pack(side= RIGHT)
        #  pack scale bar
        self.scale1.pack(side = BOTTOM, pady = 20)
        self.scale2.pack(side = BOTTOM)
        # pack panelA which is the image

        self.partcount_label.pack(side = TOP)
        self.partcount_val.pack(side = TOP)
        self.diff_label.pack(side = TOP)
        self.diff_val.pack(side = TOP)
        """Do not Seperate of Rearrange"""
        self.panelA.pack()
        self.binary_label.pack(side = TOP)
        self.binary_val.pack(side = TOP)
        self.min_label.pack(side = TOP)
        self.min_val.pack(side = TOP)
        self.avg_label.pack(side = TOP)
        self.avg_val.pack(side = TOP)
        self.partnum_label.pack(side = TOP)
        self.partnum_entry.pack(side = TOP)
        self.barcode_label.pack(side = TOP)
        self.barcode_entry.pack(side= TOP)
        self.save_button.pack(side = TOP, pady= 10)
        self.save_warning.pack(side= TOP)
        """Do not Seperate of Rearrange"""
        


# if __name__ == "__main__":
#     mainwin = Tk()
    
#     print("running view")
#     mainwin.geometry("1200x1200")
#     mainwin.title("PartCount")

#     view = View(mainwin)
#     view.setup()
#     mainwin.mainloop()
    
