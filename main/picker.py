from pynput import mouse
import time
from threading import Thread
from PIL import Image, ImageTk
from mss import mss
import threading

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
        self.updateInterval = 0.05
        self.movThreshold = 50
        
        self.lastPreviewImg = 0
        self.previewThread = None
        self.photoImage = None
        
        self.pendingUpdate = False
        
        self.threadLocal = threading.local()
        
    def closeMssInstance(self):
        if hasattr(self.threadLocal, 'sct'):
            try:
                self.threadLocal.sct.close()
            except:
                pass
            del self.threadLocal.sct
            
        
    def mssInstance(self):
        if(not hasattr(self.threadLocal, 'sct')):
            self.threadLocal.sct = mss()
        return self.threadLocal.sct

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
        
        if(self.previewThread is not None):
            self.previewThread.join(timeout=0.1)
            self.previewThread = None
            self.photoImage = None
            
        self.closeMssInstance()

    def getHex(self, rgb):
        return '%02X%02X%02X'%rgb

    #Preview Image
    def getPreviewImage(self, x, y):
        if(self.pickingPaused): return None
        
        try:
            halfSize = self.previewSize // 2
            
            bBox = (
                x - halfSize,
                y - halfSize,
                x + halfSize,
                y + halfSize
            )
            
            sct = self.mssInstance()
            img = sct.grab(bBox) 
            previewImg = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
            return previewImg 
        except Exception as e:
            print(f'Preview Error: {e}')
            return None
            
    def updateGUI(self, previewImg, currentColor):
        if(hasattr(self, 'pendingUpdate') and self.pendingUpdate): return
        self.pendingUpdate = True

        try:
            if(previewImg and self.root):
                self.photoImage = ImageTk.PhotoImage(previewImg)
                if(self.previewCallback): self.previewCallback(self.photoImage)
                if(self.liveColorCallback): self.liveColorCallback(currentColor)
        finally:
            self.pendingUpdate = False
    
    def updatePreview(self, x, y):        
        try:
            previewImg = self.getPreviewImage(x, y)
            currentColor = self.pickColor(x, y)
                
            self.root.after(0, lambda: self.updateGUI(previewImg, currentColor))
        except Exception as e:
            print(f'Preview error!: {e}')
    #
            
    def onMove(self, x, y):
        if(abs(x - self.lastX) > self.movThreshold or 
           abs(y - self.lastY) > self.movThreshold):
            self.lastX = x
            self.lastY = y
            self.lastUpdateTime = time.time()

    def pickColor(self, x, y):
        try:
            sct = self.mssInstance()
            bBox = (x, y, x + 1, y + 1)
            img = sct.grab(bBox)
            rgb = tuple(img.pixel(0, 0)[i] for i in range(3))
            return rgb
        except Exception as e:
            print(f'Color pick error: {e}')
            return(0, 0, 0)

    def onClick(self, x, y, button, pressed):        
        if(pressed and button == mouse.Button.left and not self.pickingPaused and self.callback):
            winGeometry = (
                self.root.winfo_x(),
                self.root.winfo_y(),
                self.root.winfo_width(),
                self.root.winfo_height()
            )
            
            if(winGeometry[0] <= x <= winGeometry[0] + winGeometry[2] and
               winGeometry[1] <= y <= winGeometry[1] + winGeometry[3]): 
                return False
            
            #Pick Color
            color = self.pickColor(x, y)
            if(self.callback): self.callback(color)
            return True

    def startPicking(self):
        self.stopPicking()
        
        self.pickingPaused = False
        self.isClosing = False
        
        self.listener = mouse.Listener(on_click=self.onClick, on_move=self.onMove)
        self.listener.start()
        
        self.previewThread = Thread(target=self.previewWorker)
        self.previewThread.daemon = True
        self.previewThread.start()
        
    def previewWorker(self):        
        while not self.isClosing:
            if(time.time() - self.lastUpdateTime >= self.updateInterval):
                x, y = self.lastX, self.lastY
                
                previewImg = self.getPreviewImage(x, y)
                currentColor = self.pickColor(x, y)
                
                if(previewImg is not None): self.root.after(0, lambda: self.updateGUI(previewImg, currentColor))
            time.sleep(0.01)

picker = Picker()