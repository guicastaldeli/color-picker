from tkinter import *
import os
import sys

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
        
        self.picker.previewCallback = self.preview.updatePreview
        
        self.picker.callback = self.pickColor.displayColor
        self.picker.liveColorCallback = self.liveColor.updateColor
        
        self.picker.startPicking()
        
    #Window
    def createWindow(self):
        self.root = Tk()
        self.root.title('Color Picker')
        self.root.geometry('700x330')
        self.root.attributes('-topmost', True)
        self.root.resizable(False, False)
        
        self.root.protocol('WM_DELETE_WINDOW', self.onClose)
        self.root.bind('<Unmap>', self.onMinimize)
        self.root.bind('<Map>', self.onRestore)
        
        #Icon
        self.setIcon()
        #
        
        self._preview()
        self._liveColor()
        self._pickColor()
        self._picker()
        
        #Main loop
        self.root.mainloop()
        
    #Icon
    def resourcePath(self, relativePath):
        try:
            basePath = sys._MEIPASS
        except Exception:
            basePath = os.path.abspath('.')
            
        return os.path.join(basePath, relativePath)
    
    def setIcon(self):
        try:
            iconPath = self.resourcePath(os.path.join('assets', 'icon', 'icon.ico'))
            self.root.iconbitmap(iconPath)
        except:
            iconPath = ''
    #
        
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