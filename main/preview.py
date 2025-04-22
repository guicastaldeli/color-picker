from tkinter import Canvas
from PIL import Image, ImageTk

class Preview:
    def __init__(self, parent):
        self.parent = parent
        
        #Preview Display
        self.previewImage = None
        self.previewCanvas = None
        self.currentImage = None
        self.setupPreview()
        
    def setupPreview(self):
        width = 200
        height = 200
        bg = '#212121'
        
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