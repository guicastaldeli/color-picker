from tkinter import Canvas
from PIL import Image, ImageTk
import os

class Preview:
    def __init__(self, parent):
        self.parent = parent
        
        #Preview Display
        self.previewImage = None
        self.previewCanvas = None
        self.currentImage = None
        
        #Cursor
        path = os.path.join('assets', 'img', 'ctm-cursor.png')
        self.cursorImage = ImageTk.PhotoImage(file=path)
        #
        
        self.setupPreview()
        
    def setupPreview(self):
        width = 200
        height = 200
        bg = '#212121'
        
        self.previewCanvas = Canvas(self.parent, width=width, height=height, bg=bg)
        self.previewCanvas.pack(pady=10)
        self.previewCanvas.place(x=460, y=55)
        
    def updatePreview(self, img):
        try:
            if not self.parent.winfo_viewable(): return
            if img is None: return
            
            if (hasattr(self, 'currentImage')): del self.currentImage
                
            self.currentImage = ImageTk.PhotoImage(img)
            self.previewCanvas.delete('all')
            self.previewCanvas.create_image(100, 100, image=self.currentImage)
            self.previewCanvas.create_image(100, 100, image=self.cursorImage)

        except Exception as e:
            print(f'Preview error: {e}')