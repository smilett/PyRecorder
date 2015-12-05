
from Tkinter import *

class App:
    def __init__(self, parent):       

        #------ constants for controlling layout ------
        button_width = 6      ### (1)
        
        button_padx = "2m"    ### (2)
        button_pady = "1m"    ### (2)

        buttons_frame_padx =  "3m"   ### (3)
        buttons_frame_pady =  "2m"   ### (3)        
        buttons_frame_ipadx = "3m"   ### (3)
        buttons_frame_ipady = "1m"   ### (3)
        # -------------- end constants ----------------

        self.myParent = parent 
        parent.geometry("600x400")  ### (1) Note geometry Window Manager method

        ### Our topmost frame is called myContainer1
        self.myContainer1 = Frame(parent) ###
        self.myContainer1.pack()

        # -------------- message frame ----------------
        self.message_frame = Frame(self.myContainer1) ###
        self.message_frame.pack(side=TOP, expand=NO,  padx=10, pady=5, ipadx=5, ipady=5)
        
        myMessage = "This is a recording programme"
        Label(self.message_frame, text = myMessage, justify = LEFT).pack(side = TOP, anchor = W)

        # -------------- text frame ----------------
        self.text_frame = Frame(self.myContainer1, borderwidth=2,  relief=RIDGE, height=100, width=400, background="white")
        self.text_frame.pack(side=TOP, fill=BOTH, expand=YES)

        # -------------- button frame ----------------
        self.buttons_frame = Frame(self.myContainer1)
        self.buttons_frame.pack(
            side = TOP, ipadx = buttons_frame_ipadx, ipady = buttons_frame_ipady, padx = buttons_frame_padx, pady = buttons_frame_pady)                  

        # record button
        self.button_record = Button(self.buttons_frame, command = self.button_record_Click)
        self.button_record.configure(text = "Record")
        self.button_record.focus_force()       
        self.button_record.configure(width = button_width, padx = button_padx, pady = button_pady)
        self.button_record.pack(side=LEFT)
        
        # play button
        self.button_play = Button(self.buttons_frame, command = self.button_play_Click)
        self.button_play.configure(text = "Play")  
        self.button_play.configure(width = button_width, padx = button_padx, pady = button_pady)
        self.button_play.pack(side = LEFT)

        # quit button
        self.button_quit = Button(self.buttons_frame, command = self.button_quit_Click)
        self.button_quit.configure(text = "Quit")
        self.button_quit.configure(width = button_width, padx = button_padx, pady = button_pady)
        self.button_quit.pack(side = LEFT)
                          
        
    def button_record_Click(self):
        self.myParent.destroy() 

    def button_play_Click(self):
        self.myParent.destroy() 

    def button_quit_Click(self):
        self.myParent.destroy() 


def main():
    root = Tk()
    root.wm_title("PyRecorder")
    display = App(root)
    root.mainloop()
      
if __name__ == "__main__":
    main()
  

                