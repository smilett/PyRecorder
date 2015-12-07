import time
import Tkinter as Tk

def _start():
    for outer in range(5):
        if active_stat.get():
            time.sleep(1) # some code in the real app
        else:
            active_stat.set(True)
            break
        for inner in range(5):
            if active_stat.get():
                #counterstr.set("%02d-%02d" % (outer,inner)) #does not update till the end of loop
                textbox.insert(Tk.END, "%02d-%02d\n" % (outer,inner)) #does not show till the end of loop
                print ("{}-{}".format(outer,inner))
                time.sleep(1) #some code in the real app
            else:
                active_stat.set(True)
                break
            root.update()

def _stop():
    active_stat.set(False)


root = Tk.Tk()

active_stat = Tk.BooleanVar(root)
active_stat.set(True)

#counterstr=Tk.StringVar() 
#Tk.Label(root, textvariable=counterstr).pack(side=Tk.TOP)
textbox=Tk.Text(root) 
textbox.pack(side=Tk.TOP) 
Tk.Button(root, text='Start', command=_start).pack(side=Tk.LEFT)
Tk.Button(root, text='Stop', command=_stop).pack(side=Tk.LEFT)
Tk.Button(root, text='Quit', command=root.quit).pack(side=Tk.LEFT)
root.mainloop()