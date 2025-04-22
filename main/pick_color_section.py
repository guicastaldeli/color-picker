from tkinter import Canvas, Entry, Frame, StringVar, Button, Label, ttk
from PIL import Image, ImageTk
from picker import Picker

class PickColor:
    #Init
    def __init__(self, parent):
        self.parent = parent
        self.style = ttk.Style()
        self.style.theme_use('vista')
        
        self.style.configure('Hover.TEntry', padding=0)
        self.style.map('Hover.TEntry', relief=[('hover', 'sunken')], foreground=[('hover', 'black')])
        
        self.parent.bind('<Enter>', self.onWindowEnter)
        self.parent.bind('<Leave>', self.onWindowLeave)
        
        #Main Frame        
        self.mainFrame = ttk.LabelFrame(self.parent, text='Picked Color', padding=5)
        self.mainFrame.place(x=30, y=15)
        
        #Canvas
        self.createCanvas()
        
        #Input
        self.colorRGB = StringVar(master=parent)
        self.colorHex = StringVar(master=parent)
        self.createInputs()
    
    #Window
    def onWindowEnter(self, event):
        if(hasattr(self, 'picker')): self.picker.pausePicking()
            
    def onWindowLeave(self, event):
        if(hasattr(self, 'picker')): self.picker.resumePicking()
    
    #Input
    def createInputs(self):
        self.inputFrame = Frame(self.mainFrame)
        self.inputFrame.pack(side='left', padx=(3, 0), pady=(0, 20))
        
        #RGB
        self.rgbFrame = Frame(self.inputFrame)
        self.rgbFrame.pack(side='top')
        
        ttk.Label(self.rgbFrame, text='RGB:').pack(side='top', padx=(0, 200))
        self.inputRGB = ttk.Entry(self.rgbFrame, textvariable=self.colorRGB, state='readonly', width=20, style='Hover.TEntry')
        self.inputRGB.pack(side='left')
        #
        
        #Hex
        self.hexFrame = Frame(self.inputFrame)
        self.hexFrame.pack(side='top')
        
        ttk.Label(self.hexFrame, text='Hex:').pack(side='top', padx=(0, 200))
        self.inputHex = ttk.Entry(self.hexFrame, textvariable=self.colorHex, state='readonly', width=20, style='Hover.TEntry')
        self.inputHex.pack(side='left')
        #
        
        #Buttons
        self.createButtons()
        
    #Buttons      
    def createButtons(self):
        copyText = 'Copy'
        
        #RGB
        self.rgbCopy = ttk.Button(self.rgbFrame, text=copyText, command=lambda: self.copyToClipboard(self.colorRGB.get()))
        self.rgbCopy.pack(side='left', padx=10)
        
        #Hex
        self.hexCopy = ttk.Button(self.hexFrame, text=copyText, command=lambda: self.copyToClipboard(self.colorHex.get()))
        self.hexCopy.pack(side='left', padx=10)
        
    def copyToClipboard(self, value):
        self.parent.clipboard_clear()
        self.parent.clipboard_append(value)
    
    #Canvas
    def createCanvas(self):        
        self.width = 100
        self.height = 100
        self.bg = 'black'
        
        self.colorDisplay = Canvas(self.mainFrame, width=self.width, height=self.height, bg=self.bg)
        self.colorDisplay.pack(side='right', pady=(0, 5))
        
        return self.colorDisplay
        
    #Display   
    def displayColor(self, rgb):
        textRGB = '(%d, %d, %d)' % rgb
        textHex = '#%02X%02X%02X'%rgb
        
        #Create Inputs
        _ = self.mainFrame
        
        #Set Inputs
        self.colorRGB.set(textRGB)
        self.colorHex.set(textHex)
        self.colorDisplay.config(bg=textHex)