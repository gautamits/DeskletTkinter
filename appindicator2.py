
import commands
from subprocess import call
from Tkinter import *
import Tkinter as tk
import os
import signal
import json

from urllib2 import Request, urlopen, URLError

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from desklet import *


APPINDICATOR_ID = 'myappindicator'



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

class Search():

    buttons=[]
    def search(_):
    #def __init__(self):
        self.master=Tk()
        #master.transient(master)
        #master=Win()
        #master.resizable(0,0)
        #master.overrideredirect(1)
        #Label(master, text="query").grid(row=0)
        #master.geometry('1100x30')
        self.master.minsize(1100,30)
        self.master.configure(background="#dd00dd")
        self.e1 = Entry(self.master)
        #e1 = Text(master,height=30)
        self.e1.grid(row=0,column=0)
        self.e1.bind('<Key>',self.button)
        #e1.size(1100,50)
        self.e1.pack(expand=1,fill=tk.X,ipady=3)
        self.e1.focus_set()
        self.master.mainloop()
    def addkeys(result):

        for i in buttons:
            i.destroy()
            buttons.remove(i)
        self.master.update()
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
        self.master.update()
        return 0
            #print i

    def button(event):
        #print repr(event.char),
        if event.char == " ":
            query=self.e1.get()+" "
        elif event.char.isalnum():
            query=self.e1.get()+self.event.char
        else:
            query=self.e1.get()
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



    def main(self):
        indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('icon.jpg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        indicator.set_menu(self.build_menu())
        notify.init(APPINDICATOR_ID)
        gtk.main()

    def build_menu():
        menu = gtk.Menu()

        item_joke = gtk.MenuItem('Joke')
        item_joke.connect('activate', joke)
        menu.append(item_joke)

        item_search = gtk.MenuItem('Search')
        item_search.connect('activate', Search())
        menu.append(item_search)

        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', quit)
        menu.append(item_quit)

        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', quit)
        menu.append(item_quit)


        menu.show_all()
        return menu

    def fetch_joke():
        request = Request('http://api.icndb.com/jokes/random?limitTo=[nerdy]')
        response = urlopen(request)
        joke = json.loads(response.read())['value']['joke']
        return joke

    def joke(_):
        notify.Notification.new("<b>Joke</b>", fetch_joke(), None).show()

    def quit(_):
        notify.uninit()
        gtk.main_quit()

    if __name__ == "__main__":
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        main()
