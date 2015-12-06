#coding=utf-8  

from __future__ import division  
from pyaudio import PyAudio,paInt16
from Tkinter import *
import wave
  
#define of params
CHUNK = 1024
FORMAT = paInt16
RATE = 16000
CHANNELS = 1

#record time in terms of sampling points
RECORD_SECONDS = 3
RECORD_POINTS = int(RECORD_SECONDS * RATE / CHUNK)

WAVFILE = '../wav/record.wav'

STOP = 0

##################
#                #
#      GUI       #
#                #
##################
class App:
    def __init__(self, parent):       

        self.myLastButtonInvoked = None  

        ###############################################
        #      constants for controlling layout       #
        ###############################################
        button_width = 6 
        
        button_padx = "2m"
        button_pady = "1m"

        buttons_frame_padx =  "3m"
        buttons_frame_pady =  "2m"       
        buttons_frame_ipadx = "3m"
        buttons_frame_ipady = "1m"

        ##############################
        #      set window size       #
        ##############################
        self.myParent = parent
        self.maximise()

        ### Our topmost frame is called myContainer1
        self.myContainer1 = Frame(parent)
        self.myContainer1.pack()

        ############################
        #      message frame       #
        ############################
        self.message_frame = Frame(self.myContainer1) ###
        self.message_frame.pack(side=TOP, expand=NO,  padx=10, pady=5, ipadx=5, ipady=5)
        
        myMessage = "This is a recording programme !\n"
        Label(self.message_frame, text = myMessage, justify = LEFT).pack(side = TOP, anchor = W)

        #########################
        #      text frame       #
        #########################
        self.text_frame = Frame(self.myContainer1, borderwidth=2,  relief=RIDGE, height=100, width=400, background="white")
        self.text_frame.pack(side = TOP, fill = BOTH, expand = YES)

        ###########################
        #      button frame       #
        ###########################
        self.buttons_frame = Frame(self.myContainer1)
        self.buttons_frame.pack(side = TOP, ipadx = buttons_frame_ipadx, ipady = buttons_frame_ipady, padx = buttons_frame_padx, pady = buttons_frame_pady)                  

        # record button
        self.button_record = Button(self.buttons_frame, command = self.button_record_Click)
        self.button_record.configure(text = "Record")
        self.button_record.configure(width = button_width, padx = button_padx, pady = button_pady)
        self.button_record.pack(side=LEFT)

        # stop button
        self.button_stop = Button(self.buttons_frame, command = self.button_stop_Click)
        self.button_stop.configure(text = "Stop")  
        self.button_stop.configure(width = button_width, padx = button_padx, pady = button_pady)
        #self.button_stop.configure(state = DISABLED) 
        self.button_stop.pack(side = LEFT)
        
        # play button
        self.button_play = Button(self.buttons_frame, command = self.button_play_Click)
        self.button_play.configure(text = "Play")  
        self.button_play.configure(width = button_width, padx = button_padx, pady = button_pady)
        self.button_play.configure(state = DISABLED) 
        self.button_play.pack(side = LEFT)

        # quit button
        self.button_quit = Button(self.buttons_frame, command = self.button_quit_Click)
        self.button_quit.configure(text = "Quit")
        self.button_quit.configure(width = button_width, padx = button_padx, pady = button_pady)
        self.button_quit.pack(side = LEFT)
        
        #########################
        #      foot frame       #
        #########################
        self.foot_frame = Frame(self.myContainer1) ###
        self.foot_frame.pack(side = TOP, fill = BOTH, expand = YES)
        
        ### author_frame 
        self.author_frame = Frame(self.foot_frame, borderwidth = 0,  relief=  RIDGE, width = 200) 
        self.author_frame.pack(side = LEFT, fill = BOTH, expand = YES)  
        myMessage_author = "Author: Mengxue Cao"
        Label(self.author_frame, text = myMessage_author, justify = LEFT).pack(side = LEFT, anchor = W)

        ### version_frame 
        self.version_frame = Frame(self.foot_frame, borderwidth = 0,  relief = RIDGE, width = 200)
        self.version_frame.pack(side = RIGHT,fill = BOTH, expand = YES)
        myMessage_version = "Version: 0.1"
        Label(self.version_frame, text = myMessage_version, justify = RIGHT).pack(side = RIGHT, anchor = W)
        
    def button_record_Click(self):
        #self.button_stop.configure(state = NORMAL)
        record_wave()
        self.button_play.configure(state = NORMAL)
        self.myLastButtonInvoked = "Record"

    def button_stop_Click(self):
        STOP = 1
        #self.button_stop.configure(state = DISABLED)

    def button_play_Click(self):
        #self.button_stop.configure(state = NORMAL)         
        play_wave()
        self.myLastButtonInvoked = "Play"

    def button_quit_Click(self):
        self.myParent.destroy()

    def maximise (self):
        w, h = self.myParent.winfo_screenwidth(), self.myParent.winfo_screenheight()
        width = w * 0.6
        hight = h * 0.6
        left_blank = (w - width) / 2
        top_blank = (h - hight) / 2
        self.myParent.geometry("%dx%d+%d+%d" % (width, hight, left_blank, top_blank))


##################
#                #
#   RECORDING    #
#                #
##################
def save_wave_file(filename, data, sampwidth):
    '''''save the data to the wav file'''
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(sampwidth)
    wf.setframerate(RATE)
    wf.writeframes("".join(data))
    wf.close()
      
def record_wave():
    #open the input of wave
    wav_in = PyAudio()

    stream = wav_in.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)
    
    print("* recording")

    save_buffer = []
    count = 0
    
    while count < RECORD_POINTS:
        #read CHUNK sampling data
        string_audio_data = stream.read(CHUNK)
        save_buffer.append(string_audio_data)        
        print '.'
        count += 1
    
    sampwidth = wav_in.get_sample_size(FORMAT)
    save_wave_file(WAVFILE, save_buffer, sampwidth)
    save_buffer = []

    print WAVFILE, "saved"

##################
#                #
#    PLAYING     #
#                #
##################
def play_wave():
    wf = wave.open(WAVFILE, 'rb')

    wav_out = PyAudio()

    # open stream (2)
    stream = wav_out.open(format = wav_out.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)
    
    data = wf.readframes(CHUNK) # read data

    # play stream (3)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    wav_out.terminate() 

##################
#                #
#      MAIN      #
#                #
##################
def main():
    root = Tk()
    root.wm_title("PyRecorder")
    display = App(root)
    root.mainloop()      
      
if __name__ == "__main__":
    main()