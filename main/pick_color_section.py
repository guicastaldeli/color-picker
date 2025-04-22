from tkinter import Canvas, Entry, Frame, StringVar, Button, Label
from PIL import Image, ImageTk
from picker import Picker

class PickColor:
    #Init
    def __init__(self, parent):
        self.parent = parent
        
        self.parent.bind('<Enter>', self.onWindowEnter)
        self.parent.bind('<Leave>', self.onWindowLeave)
        
        #Display Color
        self.colorDisplay = self.createCanvas(parent)
        
        #Input
        self.inputFrame = None
        self.inputRGB = None
        self.inputHex = None
        self.colorRGB = StringVar(master=parent)
        self.colorHex = StringVar(master=parent)
        self.createInputs()
        
        #Buttons
        self.rgbFrame = None
        self.hexFrame = None
        self.rgbCopy = None
        self.hexCopy = None
    
    #Window
    def onWindowEnter(self, event):
        if(hasattr(self, 'picker')): self.picker.pausePicking()
            
    def onWindowLeave(self, event):
        if(hasattr(self, 'picker')): self.picker.resumePicking()
    
    #Input
    def createInputs(self):
        self.inputFrame = Frame(self.parent)
        self.inputFrame.pack(pady=0)
        
        #RGB
        self.rgbFrame = Frame(self.inputFrame)
        self.rgbFrame.pack(side='left', padx=10)
        
        Label(self.rgbFrame, text='RGB:').pack(side='left', padx=(0, 5))
        self.inputRGB = Entry(self.rgbFrame, textvariable=self.colorRGB, state='readonly', width=10)
        self.inputRGB.pack(side='left')
        #
        
        #Hex
        self.hexFrame = Frame(self.inputFrame)
        self.hexFrame.pack(side='left', padx=10)
        
        Label(self.hexFrame, text='Hex:').pack(side='left', padx=(0, 5))
        self.inputHex = Entry(self.hexFrame, textvariable=self.colorHex, state='readonly', width=10)
        self.inputHex.pack(side='left')
        #
        
        #Buttons
        self.createButtons()
        
    #Button        
    def createButtons(self):
        copyText = 'Copy'
        
        #RGB
        self.rgbCopy = Button(self.rgbFrame, text=copyText, command=lambda: self.copyToClipboard(self.colorRGB.get()))
        self.rgbCopy.pack(side='left', padx=5)
        
        #Hex
        self.hexCopy = Button(self.hexFrame, text=copyText, command=lambda: self.copyToClipboard(self.colorHex.get()))
        self.hexCopy.pack(side='left', padx=5)
        
    def copyToClipboard(self, value):
        self.parent.clipboard_clear()
        self.parent.clipboard_append(value)
    
    #Canvas
    def createCanvas(self, parent):
        self.width = 100
        self.height = 100
        self.bg = 'white'
        
        self.colorDisplay = Canvas(parent, width=self.width, height=self.height, bg=self.bg)
        self.colorDisplay.pack(pady=0)
        
        return self.colorDisplay
        
    #Display   
    def displayColor(self, rgb):
        textRGB = '%d, %d, %d' % rgb
        textHex = '#%02X%02X%02X'%rgb
        
        #Create Inputs
        _ = self.inputFrame
        
        #Set Inputs
        self.colorRGB.set(textRGB)
        self.colorHex.set(textHex)
        self.colorDisplay.config(bg=textHex)