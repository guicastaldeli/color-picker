from tkinter import *

from picker import Picker
from ui import UI

class Main:    
    #UI
    def _ui(self):
        self.ui = UI(self.root)
    
    #Picker
    def _picker(self):
        self.picker = Picker()
        self.picker.root = self.root
        self.ui.picker = self.picker
        
        self.canvas = self.ui.createCanvas(self.root)
        self.picker.callback = self.ui.displayColor
        self.picker.previewCallback = self.ui.updatePreview
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
        
        #UI
        self._ui()
        
        #Picker
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