from pynput import mouse
from PIL import Image, ImageGrab

class Picker:
    def main(self):
        self.listener = None
        self.callback = None
        
    def getHex(self, rgb):
        return '%02X%02X%02X'%rgb
        
    def pickColor(self, x, y):        
        bBox = (x, y, x + 1, y + 1)
        img = ImageGrab.grab(bbox=bBox)
        rgb = img.convert('RGB')
        
        #RGB
        rgb = rgb.getpixel((0, 0))
        
        print(f'COLOR: rgb({rgb}) | HEX #{self.getHex(rgb)}')
        
        return rgb
        
    def onClick(self, x, y, button, pressed):        
        if pressed and button == mouse.Button.left:
            color = self.pickColor(x, y)
            if self.callback: self.callback(color)
            return False
        
    def startPicking(self):
        call = None
        
        self.callback = call
        self.listener = mouse.Listener(on_click=self.onClick)
        self.listener.start()
            
picker = Picker()