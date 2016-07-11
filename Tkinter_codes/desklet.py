import commands
from subprocess import call
from Tkinter import *
import Tkinter as tk

############################################################# for floating window #######################################################
class Win(tk.Tk):

    def __init__(self,master=None):
        tk.Tk.__init__(self,master)
        self.overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        self.bind('<Button-1>',self.clickwin)
        self.bind('<B1-Motion>',self.dragwin)

    def dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y


########################################################## for tooltip ##########################################################

class CreateToolTip(object):
    '''
    create a tooltip for a given widget
    '''
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background='green', relief='solid', borderwidth=1,
                       font=("times", "12", "normal"))
        label.pack(ipadx=1)
    def close(self, event=None):
        if self.tw:
            self.tw.destroy()



buttons=[]
def addkeys(result):

	for i in buttons:
		i.destroy()
		buttons.remove(i)
		master.update()
	for i in result:
		t=i.split('/')
		t=t[len(t)-1]
		#b=Button(master,text=t,command=lambda i=i:commands.getstatusoutput("xdg-open "+i))
		#b=Button(master,text=t,width=25,command=lambda i=i:call(["xdg-open",i]))
		b=Button(master,text=t,command=lambda i=i:call(["xdg-open",i]))
		#b.grid(column=0,row=j)
		b.pack(expand=1,fill=tk.X)
		b_ttp=CreateToolTip(b,i)
		buttons.append(b)
	master.update()
	return 0
		#print i

def button(event):
	#print repr(event.char),
	if event.char == " ":
		query=e1.get()+" "
	elif event.char.isalnum():
		query=e1.get()+event.char
	else:
		query=e1.get()
	query='"'+query+'"'
	if len(query)>=7:
		command='locate -i '+query+' | grep -e "/mnt" -e "/media" -e "/home" | grep -v "/\." | grep -v "android" | grep -v "Android" | grep -v "workspace"'
		#print command
		result=commands.getstatusoutput(command)
		
		a,result=result
		result=result.split('\n')
		result=result[:15]
		addkeys(result)
		return 0
	else:
		for i in buttons:
			i.destroy()
			buttons.remove(i)
			master.update()

master=Tk()
#master.transient(master)
#master=Win()
#master.resizable(0,0)
#master.overrideredirect(1)
#Label(master, text="query").grid(row=0)
#master.geometry('1100x30')
master.minsize(1100,30)
master.configure(background="#dd00dd")
e1 = Entry(master)
#e1 = Text(master,height=30)
e1.grid(row=0,column=0)
e1.bind('<Key>',button)
#e1.size(1100,50)
e1.pack(expand=1,fill=tk.X,ipady=3)
e1.focus_set()
master.mainloop()