from pynput import mouse
import time
from threading import Thread
from PIL import Image, ImageGrab, ImageTk
import numpy as np

class Picker:
    #Init
    def __init__(self):
        self.listener = None
        self.root = None
        self.isClosing = False
        
        self.pickingPaused = False
        
        self.callback = None
        self.previewCallback = None
        self.liveColorCallback = None
        
        self.lastY = 0
        self.lastX = 0
        
        self.previewSize = 200
        self.lastUpdateTime = 0
        self.updateInterval = 0.1
        self.movThreshold = 30
        
        self.active = True
        self.previewThread = None
        self.lastPreviewImg = None
        self.photoImage = None

    def pausePicking(self):
        self.pickingPaused = True

    def resumePicking(self):
        self.pickingPaused = False
        self.listener = mouse.Listener(on_click=self.onClick, on_move=self.onMove)
        self.listener.start()

    def stopPicking(self):
        self.active = False
        
        if(self.listener):
            self.listener.stop()
            self.listener = None
        self.pickingPaused = True
        
        if(self.previewThread is not None):
            self.previewThread.join(timeout=0.1)
            self.previewThread = None

    def getHex(self, rgb):
        return '%02X%02X%02X'%rgb

    #Preview Image
    def getPreviewImage(self, x, y):
        if(self.pickingPaused or not self.active): return
        
        try:
            halfSize = self.previewSize / 2
            
            bBox = (
                int(x - halfSize),
                int(y - halfSize),
                int(x + halfSize),
                int(y + halfSize)
            )
            
            with ImageGrab.grab(bbox=bBox) as img:
                previewImg = img.resize((200, 200), Image.Resampling.NEAREST)
                centerColor = img.getpixel((img.width // 2, img.height // 2))
                if(self.root and self.active): self.root.after(0, lambda: self.updateGUI(previewImg, centerColor))
                
                return previewImg
        except Exception as e:
            print(f'Preview Error: {e}')
            
    def updateGUI(self, previewImg, color):
        if(self.previewCallback):
            try:                
                self.photoImage = ImageTk.PhotoImage(previewImg)
                self.previewCallback(self.photoImage)
            except Exception as e:
                print(f'Error updating GUI: {e}')
            
        if(self.liveColorCallback):
            try:
                self.liveColorCallback(color)
            except:
                pass

    def onMove(self, x, y):
        if(abs(x - self.lastX) < self.movThreshold and abs(y - self.lastY) < self.movThreshold): return
        
        currentTime = time.time()
        if(currentTime - self.lastUpdateTime < self.updateInterval): return
        
        self.lastX = x
        self.lastY = y
        self.lastUpdateTime = currentTime
        
        if(self.previewThread is None or not self.previewThread.is_alive()):
            self.previewThread = Thread(target=self.updatePreview, args=(x, y))
            self.previewThread.daemon = True
            self.previewThread.start()

    def updatePreview(self, x, y):
        if(not self.pickingPaused):
            try:
                previewImg = self.getPreviewImage(x, y)
                currentColor = self.pickColor(x, y)
                
                if(self.previewCallback and self.root): self.root.after(0, lambda: self.updateGUI(previewImg, currentColor))
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