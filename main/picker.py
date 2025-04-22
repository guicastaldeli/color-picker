from pynput import mouse
import time
from threading import Thread
from PIL import Image, ImageGrab, ImageTk
import numpy as np

class Picker:
    #Init
    def __init__(self):
        self.listener = None
        self.callback = None
        self.pickingPaused = False
        self.root = None
        self.isClosing = False
        
        self.previewCallback = None
        self.previewSize = 200
        self.magnification = 3
        self.lastUpdateTime = 0
        self.updateInterval = 0.1
        self.lastY = 0
        self.lastX = 0
        self.movThreshold = 20
        
    def pausePicking(self):
        self.pickingPaused = True
        
    def resumePicking(self):
        self.pickingPaused = False
        self.listener = mouse.Listener(on_click=self.onClick, on_move=self.onMove)
        self.listener.start()
            
        
    def stopPicking(self):
        if(self.listener):
            self.listener.stop()
            self.listener = None
        self.pickingPaused = True
        
    def getHex(self, rgb):
        return '%02X%02X%02X'%rgb
    
    #Preview Image
    def getPreviewImage(self, x, y):
        halfSize = self.previewSize / 2
        
        bBox = (
            x - halfSize,
            y - halfSize,
            x + halfSize,
            y + halfSize
        )
        
        img = ImageGrab.grab(bbox=bBox)
        
        return img.resize((200, 200), Image.Resampling.LANCZOS)
    
    def onMove(self, x, y):
        currentTime = time.time()
        if(currentTime - self.lastUpdateTime < self.updateInterval): return
        elapsed = currentTime - self.lastUpdateTime
        
        if(elapsed >= self.updateInterval):
            self.lastUpdateTime = currentTime
            Thread(target=self.updatePreview, args=(x, y)).start()
        
    def updatePreview(self, x, y):
        if(not self.pickingPaused and self.previewCallback):
            try:
                previewImg = self.getPreviewImage(x, y)
                self.root.after(0, lambda: self.previewCallback(previewImg))
            except Exception as e:
                print(f'Preview error!: {e}')
        
    def pickColor(self, x, y):        
        bBox = (x, y, x + 1, y + 1)
        img = ImageGrab.grab(bbox=bBox)
        rgb = img.convert('RGB')
        
        #RGB
        rgb = rgb.getpixel((0, 0))
        
        return rgb
        
    def onClick(self, x, y, button, pressed):        
        if(pressed and button == mouse.Button.left and not self.pickingPaused and self.callback):
            winX = self.root.winfo_x()
            winY = self.root.winfo_y()
            winWidth = self.root.winfo_width()
            winHeight = self.root.winfo_height()
            
            if(winX <= x <= winX + winWidth and winY <= y <= winY + winHeight): return False
            
            color = self.pickColor(x, y)
            if(self.callback): self.callback(color)
            return True
        
    def startPicking(self):
        self.stopPicking()
        self.pickingPaused = False
        self.isClosing = False
        self.listener = mouse.Listener(on_click=self.onClick, on_move=self.onMove)
        self.listener.start()
            
picker = Picker()