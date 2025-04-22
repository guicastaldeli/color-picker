from tkinter import *
import os

from live_color_section import LiveColor
from pick_color_section import PickColor
from preview import Preview
from picker import Picker

class Main:
    #Live Color Section
    def _liveColor(self):
        self.liveColor = LiveColor(self.root)
    
    #Pick Color Section
    def _pickColor(self):
        self.pickColor = PickColor(self.root)
        
    #Preview
    def _preview(self):
        self.preview = Preview(self.root)
        
    #Picker
    def _picker(self):
        self.picker = Picker()
        self.picker.root = self.root
        self.pickColor.picker = self.picker
        
        self.picker.callback = self.pickColor.displayColor
        self.picker.previewCallback = self.preview.updatePreview
        self.picker.startPicking()
        
    #Window
    def createWindow(self):
        self.root = Tk()
        self.root.title('Color Picker')
        self.root.geometry('800x400')
        self.root.attributes('-topmost', True)
        
        self.root.protocol('WM_DELETE_WINDOW', self.onClose)
        self.root.bind('<Unmap>', self.onMinimize)
        self.root.bind('<Map>', self.onRestore)
        
        self._liveColor
        self._pickColor()
        self._preview()
        self._picker()
        
        #Main loop
        self.root.mainloop()
        
    def onClose(self):
        self.picker.isClosing = True
        self.picker.stopPicking()
        self.root.destroy()
        
    def onMinimize(self, event):
        self.picker.pausePicking()
        
    def onRestore(self, event):
        if(not self.picker.pickingPaused): self.picker.resumePicking()
        
    #Init
    def __init__(self):
        self.root = None
        self.createWindow()

main = Main()