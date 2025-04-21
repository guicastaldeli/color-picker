from tkinter import Canvas, Entry, Frame, StringVar, Button
from PIL import Image, ImageTk
from picker import Picker

class UI:
    #Init
    def __init__(self, parent):
        self.parent = parent
        
        self.parent.bind('<Enter>', self.onWindowEnter)
        self.parent.bind('<Leave>', self.onWindowLeave)
        
        #Display Color
        self.colorDisplay = self.createCanvas(parent)
        
        #Preview Display
        self.previewImage = None
        self.previewCanvas = None
        self.setupPreview()
        
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
        self.createButtons()
    
    #Window
    def onWindowEnter(self, event):
        if(hasattr(self, 'picker')): self.picker.pausePicking()
            
    def onWindowLeave(self, event):
        if(hasattr(self, 'picker')): self.picker.resumePicking()
        
    #Preview Display
    def setupPreview(self):
        width = 200
        height = 200
        bg = 'white'
        
        self.previewCanvas = Canvas(self.parent, width=width, height=height, bg=bg)
        self.previewCanvas.pack(pady=10)
        
    def updatePreview(self, img):
        try:
            if not self.parent.winfo_viewable(): return
                
            self.currentImage = ImageTk.PhotoImage(img)
            self.previewCanvas.delete('all')
            self.previewCanvas.create_image(100, 100, image=self.currentImage)
        except Exception as e:
            print(f'Preview error: {e}')
    
    #Input
    def createInputs(self):
        inputFrame = Frame(self.parent)
        inputFrame.pack(pady=10)
        
        #RGB
        self.rgbFrame = Frame(self.inputFrame)
        self.inputRGB = Entry(inputFrame, textvariable=self.colorRGB, state='readonly', width=10)
        self.inputRGB.pack(side='left', padx=5)
        
        #Hex
        self.hexFrame = Frame(self.inputFrame)
        self.inputHex = Entry(inputFrame, textvariable=self.colorHex, state='readonly', width=10)
        self.inputHex.pack(side='left', padx=5)
        
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
        self.colorDisplay.pack(pady=20)
        
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