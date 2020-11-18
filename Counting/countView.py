import tkinter as tk
from tkinter import *
from pubsub import pub
import PIL.Image, PIL.ImageTk

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
        self.leftFrame = Frame(self.container, borderwidth =2, highlightbackground = "black",
            highlightcolor = "red", highlightthickness = 1, width = 700, height = 700)
        self.rightFrame = Frame(self.container, borderwidth =2, highlightbackground = "black",
            highlightcolor = "red", highlightthickness = 1, width = 700, height = 600)
        self.toptopFrame = Frame(self.topFrame)
        self.topbotFrame = Frame(self.topFrame)
        self.topbotleftFrame = Frame(self.topbotFrame)
        self.topbotRightFrame = Frame(self.topbotFrame)


        self.current_label = tk.Label(self.toptopFrame, text = "Current Part : None", width = 200, font =( "tkDefaultFont", 44))

        self.barcode_label = tk.Label (self.topbotleftFrame, text = "Enter barcode number: ", width = 20, anchor=W , justify=LEFT)
        self.barcode_entry = tk.Entry(self.topbotleftFrame)

        self.partnum_label = tk.Label (self.topbotleftFrame, text = "Enter Part number: ", width = 20, anchor=W , justify=LEFT)
        self.partnum_entry = tk.Entry(self.topbotleftFrame)

        self.load_button = tk.Button (self.topbotRightFrame, text = "Load program", command = self.findProg)
        self.load_result = tk.Label(self.topbotRightFrame, text = "Enter a barcode or part number to search")

        """from herer"""
        self.canvas = tk.Canvas(self.leftFrame, width = 1000, height = 600)

        self.count_label = tk.Label(self.rightFrame, text = "Count", font= ( "tkDefaultFont", 44), anchor=W , justify=LEFT)
        self.count_results = tk.Label(self.rightFrame, text = "0", font= ( "tkDefaultFont", 44))

        self.incorrect_part_label = tk.Label(self.rightFrame, text = "", font= ( "tkDefaultFont", 44), bg = "white", anchor = W, justify = LEFT, wraplength = 300)
        self.severe_overlap_label = tk.Label(self.rightFrame, text = "", font= ( "tkDefaultFont", 44), bg = "white", anchor = W, justify = LEFT, wraplength = 300)
        
        self.save_button = tk.Button(self.rightFrame, text = "Save Image", command = self.saveImg)

    def updateCanvas(self, frame) : 
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas.create_image(500,300, image = self.photo)

    def saveImg(self) : 
        pub.sendMessage("Save_Img_Button_Pressed")

    def findProg(self): 
        self.load_result['text'] = "Program Loaded"
        pub.sendMessage("Find_Prog_Button_pressed")
        print("Pressed")
    
    def count_update(self, data) : 
        self.count_results['text'] = f"{data}"

    def prog_label_update(self, data) : 
        self.load_result['text'] = f"{data}"
    
    def current_label_update(self, data) : 
        self.current_label['text'] = f"{data}"

    def severe_overlap_update (self, data1, data2) : 
        self.severe_overlap_label['text'] = f"{data1}"
        self.severe_overlap_label['bg'] = f"{data2}"

    def incorrect_program_update (self, data1, data2) : 
        self.incorrect_part_label['text'] = f"{data1}"
        self.incorrect_part_label['bg'] = f"{data2}"   


    def setup_layout(self) : 
        self.topFrame.pack(side = TOP)
        self.leftFrame.pack(side = LEFT)
        self.rightFrame.pack(side = RIGHT)
        self.toptopFrame.pack(side = TOP)
        self.topbotFrame.pack(side = BOTTOM)
        self.topbotleftFrame.pack(side = LEFT)
        self.topbotRightFrame.pack(side = RIGHT)


        self.current_label.pack(side = TOP)
        self.barcode_label.pack(side = TOP)
        self.barcode_entry.pack(side = TOP)
        self.partnum_label.pack(side= TOP)
        self.partnum_entry.pack(side = TOP)
        self.load_button.pack(side= TOP, padx = 50)
        self.load_result.pack(side = TOP)


        self.canvas.pack(side = LEFT, padx = 30)
        self.save_button.pack(side = TOP)
        self.count_label.pack(side = TOP)
        self.count_results.pack(side = TOP)
        self.incorrect_part_label.pack(side = TOP, pady = 30)
        self.severe_overlap_label.pack(side = TOP, pady= 30 )






    
