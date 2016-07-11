from Tkinter import *


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
    def raise_frame(self,frame):
    	frame.tkraise()   
        
    def initUI(self):
      
        self.parent.title("Simple menu")
        ####### top menu ###############
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        exitMenu = Menu(menubar)
        helpMenu = Menu(menubar)

        

        #fileMenu.add_command(label="Included Paths",command=self.onExit)
        fileMenu.add_command(label="Included Paths",command=lambda:self.raise_frame(addfolders))
        fileMenu.add_command(label="Ignored Paths",command=self.onExit)
        fileMenu.add_command(label="Refresh database",command=self.onExit)

        helpMenu.add_command(label="About",command=self.onExit)
        helpMenu.add_command(label="Contact Me",command=self.onExit)


        exitMenu.add_command(label="Exit", command=self.onExit)


        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label="About",menu=helpMenu)
        menubar.add_cascade(label="Exit",menu=exitMenu)


    	addfolders = Frame(self.parent)
    	label=Label(addfolders,textvariable="folder adding frame",relief=RAISED)
    	label.pack()
    	self.parent.update()

        

    def onExit(self):
        self.quit()
    


def main():
  
    root = Tk()
    root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()    
