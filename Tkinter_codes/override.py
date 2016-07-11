import Tkinter
class App:
    def __init__(self):
        self.root = Tkinter.Tk()
        Tkinter.Label(self.root, text="main window").pack()
        self.window = Tkinter.Toplevel()
        self.window.overrideredirect(1)
        Tkinter.Label(self.window, text="Additional window").pack()
        self.root.bind("<Unmap>", self.OnUnMap)
        self.root.bind("<Map>", self.OnMap)
        self.root.mainloop()
    def OnMap(self, e):
        self.window.wm_deiconify()
    def OnUnMap(self, e):
        self.window.wm_withdraw()
app=App()