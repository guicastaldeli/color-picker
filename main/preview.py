from tkinter import ttk, Canvas
from PIL import ImageTk
import os
import sys

class Preview:
    def __init__(self, parent):
        self.parent = parent
        
        #Style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#dcdcdc')
        #
        
        #Preview Display
        self.previewCanvas = None
        self.currentImage = None
        
        #Cursor
        self.setCursor()
        
        #Separator
        self.setSeparator()
        
        #Preview
        self.setupPreview()
        
    def resourcePath(self, relativePath):
        try:
            basePath = sys._MEIPASS
        except Exception:
            basePath = os.path.abspath('.')
        
        return os.path.join(basePath, relativePath)
        
    def setSeparator(self):
        self.separator = ttk.Separator(self.parent, style='TFrame')
        self.separator.place(x=415, y=40, width=1, height=250)
        
    def setCursor(self):
        try:
            path = self.resourcePath(os.path.join('assets', 'img', 'ctm-cursor.png'))
            self.cursorImage = ImageTk.PhotoImage(file=path)
        except Exception as e:
            self.cursorImage = ''
        
    def setupPreview(self):
        width = 200
        height = 200
        bg = '#212121'
        
        self.previewCanvas = Canvas(self.parent, width=width, height=height, bg=bg, bd=0, highlightthickness=0)
        self.previewCanvas.pack(pady=10)
        self.previewCanvas.place(x=460, y=55)
        
    def updatePreview(self, img):
        try:
            if img is None: return
                
            self.currentImage = img
            self.previewCanvas.delete('all')
            self.previewCanvas.create_image(100, 100, image=self.currentImage)
            if(hasattr(self, 'cursorImage')): self.previewCanvas.create_image(100, 100, image=self.cursorImage)

        except Exception as e:
            print(f'Preview error: {e}')