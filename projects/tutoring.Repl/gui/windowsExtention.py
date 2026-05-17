import tkinter as tk
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.up = tk.Button(self)
        self.up["text"] = "▲"
        self.up["command"] = self.doUp
        self.up.pack(side="top")
        
        self.down = tk.Button(self)
        self.down["text"] = "▼"
        self.down["command"] = self.doDown
        self.down.pack(side="bottom")
    
        self.left = tk.Button(self)
        self.left["text"] = "◄"
        self.left["command"] = self.doLeft
        self.left.pack(side="left")
        
        self.right = tk.Button(self)
        self.right["text"] = "►"
        self.right["command"] = self.doRight
        self.right.pack(side="right")

        self.quit = tk.Button(self)
        self.quit["text"] = "QUIT"
        self.quit["command"] = self.master.destroy
        self.quit.pack(side="bottom")

    def doUp(self):
        keyboard.press(Key.alt_l)
        time.sleep(.25)
        keyboard.press(Key.tab)
        time.sleep(.25)
        keyboard.release(Key.tab)
        time.sleep(.25)
        keyboard.press(Key.tab)
        time.sleep(.25)
        keyboard.release(Key.tab)
        time.sleep(.25)
        keyboard.release(Key.alt_l)
        time.sleep(.25)

        keyboard.press(Key.cmd)
        time.sleep(.25)
        keyboard.press(Key.up)
        time.sleep(.25)
        keyboard.release(Key.up)
        time.sleep(.25)
        keyboard.release(Key.cmd)
        
    def doDown(self):
        keyboard.press(Key.alt_l)
        time.sleep(.25)
        keyboard.press(Key.tab)
        time.sleep(.25)
        keyboard.release(Key.tab)
        time.sleep(.25)
        keyboard.press(Key.tab)
        time.sleep(.25)
        keyboard.release(Key.tab)
        time.sleep(.25)
        keyboard.release(Key.alt_l)
        time.sleep(.25)

        keyboard.press(Key.cmd)
        time.sleep(.25)
        keyboard.press(Key.down)
        time.sleep(.25)
        keyboard.release(Key.down)
        time.sleep(.25)
        keyboard.release(Key.cmd)

    def doLeft(self):
        keyboard.press(Key.alt_l)
        time.sleep(.25)
        keyboard.press(Key.tab)
        time.sleep(.25)
        keyboard.release(Key.tab)
        time.sleep(.25)
        keyboard.press(Key.tab)
        time.sleep(.25)
        keyboard.release(Key.tab)
        time.sleep(.25)
        keyboard.release(Key.alt_l)
        time.sleep(.25)

        keyboard.press(Key.cmd)
        time.sleep(.25)
        keyboard.press(Key.left)
        time.sleep(.25)
        keyboard.release(Key.left)
        time.sleep(.25)
        keyboard.release(Key.cmd)

    def doRight(self):
        keyboard.press(Key.alt_l)
        time.sleep(.25)
        keyboard.press(Key.tab)
        time.sleep(.25)
        keyboard.release(Key.tab)
        time.sleep(.25)
        keyboard.press(Key.tab)
        time.sleep(.25)
        keyboard.release(Key.tab)
        time.sleep(.25)
        keyboard.release(Key.alt_l)
        time.sleep(.25)

        keyboard.press(Key.cmd)
        time.sleep(.25)
        keyboard.press(Key.right)
        time.sleep(.25)
        keyboard.release(Key.right)
        time.sleep(.25)
        keyboard.release(Key.cmd)

    # def exit(self):
    #     keyboard.type("exit")
    #     keyboard.press(Key.enter)
    #     keyboard.release(Key.enter)


root = tk.Tk()
app = Application(master=root)
app.mainloop()