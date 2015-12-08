from Tkinter import *

master = Tk()

v = StringVar()
Label(master, textvariable=v).pack()

v.set("New Text!")

v.set("New 1!")

mainloop()