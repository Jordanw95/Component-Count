from hnzView import View
from hnzModel import Model, DataStore
from tkinter import *
from pubsub import pub

class Controller :
    def __init__(self, parent): #Parent is the tkinter main window
        #variables
        self.parent = parent
        self.model = Model() #point to model object
        self.datastore = DataStore()
        self.view = View(parent)
        self.view.setup()

        pub.subscribe(self.openfile_btn_pressed, "OpenFile_Button_Pressed")
        pub.subscribe(self.original_btn_pressed, "OriginalImg_Button_Pressed")
        pub.subscribe(self.scalar_bin_change_btn_pressed, "ScalarBinChange_Button_Pressed")
        pub.subscribe(self.saveref_btn_pressed, "SaveRef_Button_Pressed")
        pub.subscribe(self.scalar_min_change_btn_pressed, "ScalarMinChange_Button_Pressed")

        # This will hadle all situation when Model has been changed to refresh View or values
        pub.subscribe(self.model_change_handler, "model_updated")
        pub.subscribe(self.average_value_update, "average_value")
        pub.subscribe(self.set_check, "setting_check")

    def openfile_btn_pressed(self) : 
        # print ("Controller - open file button pressed.")
        self.model.loadImg()

    def original_btn_pressed(self) : 
        print ("Controller - original button pressed")
        self.model.original_img()
        self.datastore.view_all()
    
    def scalar_bin_change_btn_pressed(self) : 
        self.model.binarise_img(self.view.scale1.get())
        self.model.find_average(self.view.scale1.get(), self.view.scale2.get())
        print("Controller - scalar change bar scrolled")

    def scalar_min_change_btn_pressed(self) : 
        self.model.find_average(self.view.scale1.get(), self.view.scale2.get())
        print("Controller - scalar change bar scrolled")

    def saveref_btn_pressed(self):
        refdata = [self.view.partnum_entry.get(),
            self.view.barcode_entry.get(),
            self.view.avg_val["text"], 
            self.view.binary_val["text"],
            self.view.min_val["text"]]
        if not "" in refdata :
            self.datastore.add_entry(self.view.partnum_entry.get(),
                self.view.barcode_entry.get(),
                self.view.avg_val["text"], 
                self.view.binary_val["text"],
                self.view.min_val["text"])
        else :
            self.view.savemissingfields()
        self.datastore.view_all()
        

    def model_change_handler(self, data) : 
        self.view.updateImg(data)
        print("Controller gets here")

    def average_value_update(self, data) :
        self.view.updateAverage(data)

    def set_check(self, data) : 
        self.view.set_check_update(data)


#application entry point main method
    #create instance of tk
if __name__ == "__main__":
    mainwin = Tk()
    print("running view")
    mainwin.geometry("1100x750")
    mainwin.title("PartReference")

    app = Controller(mainwin)
    mainwin.mainloop()