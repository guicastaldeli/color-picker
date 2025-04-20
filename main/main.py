from tkinter import *
from picker import Picker

class Main:
    #Picker
    def _picker(self):
        self.picker = Picker()
        
    #Window Configs
    def window(self):
        self.root = Tk()
        self.root.title('Color Picker')
        self.root.geometry('800x400')
        
        self.button = Button(self.root, text='Pick Color', command=self.picker.startPicking)
        self.button.pack(pady=20)
        
        self.root.mainloop()
        
    #Init
    def __init__(self):
        self._picker()
        self.window()

main = Main()