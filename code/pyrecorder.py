#coding=utf-8  

from __future__ import division  
from pyaudio import PyAudio,paInt16
from Tkinter import *
import wave
  
# define of parameters
CHUNK = 1024        # frames per buffer
FORMAT = paInt16    # bit rate: 16-bit > paInt16, 32-bit > paInt32
RATE = 44100        # sampling rate
CHANNELS = 1

WAVFILE = '../wav/record.wav'
SCRIPT_FILE = '../script/script'


####################
#                  #
#    RED SCRIPT    #
#                  #
#################### 

# read data from file
def read_file(filename):
    f = open(filename)  # open the file and read
    s = f.read()        # convert the content into string 
    f.close()           # close the file
    
    l = s.split('\n')

    return l


##################
#                #
#   RECORDING    #
#                #
##################

# do record
def record():
    global state
    global save_buffer
    global stream_in

    if state == 1:                            
        string_audio_data = stream_in.read(CHUNK)
        save_buffer.append(string_audio_data)        

        #pause = int(100*CHUNK/RATE)
        root.after(1, record)

# save waveform into wav file
def save_wave_file(filename, data_in, sampwidth):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(sampwidth)
    wf.setframerate(RATE)
    wf.writeframes("".join(data_in))
    wf.close()

##################
#                #
#    PLAYING     #
#                #
##################

# play the audio
def play_wave():
    global state
    global data_out
    global stream_out
    global wav_out
    global wave_form

    if len(data_out) == 0:
        stream_out.stop_stream()
        stream_out.close()
        wav_out.terminate()

    elif state == 2:
        stream_out.write(data_out)
        data_out = wave_form.readframes(CHUNK)

        root.after(1, play_wave)     


#######################
#                     #
#    BUTTON CLICK     #
#                     #
#######################

def button_record_Click():
    global sampwidth
    global wav_in
    global stream_in
    global state

    state = 1
    button_stop.configure(state = NORMAL)     

    wav_in = PyAudio()
    stream_in = wav_in.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK) 
    sampwidth = wav_in.get_sample_size(FORMAT)
    print("* recording")
    record() 


def button_play_Click():
    global state
    global wav_out
    global stream_out
    global data_out
    global wave_form

    state = 2
    button_stop.configure(state = NORMAL)

    wav_out = PyAudio()

    wave_form = wave.open(WAVFILE, 'rb')

    stream_out = wav_out.open(format = wav_out.get_format_from_width(wave_form.getsampwidth()),
                channels = wave_form.getnchannels(),
                rate = wave_form.getframerate(),
                output = True)
    
    data_out = wave_form.readframes(CHUNK) # read data
    play_wave()
   
def button_stop_Click():
    global state
    global save_buffer
    global wav_in
    global wav_out
    global stream_in
    global stream_out
    global data_out

    # stop fron recording
    if state == 1:
        state = 0
        save_wave_file(WAVFILE, save_buffer, sampwidth)

        # clean up
        save_buffer = []
        stream_in.stop_stream()
        stream_in.close()
        wav_in.terminate() 

        button_stop.configure(state = DISABLED)
        button_play.configure(state = NORMAL)

    # stop from playing
    elif state == 2:
        state = 0
        stream_out.stop_stream()
        stream_out.close()
        wav_out.terminate() 
        data_out = []

        button_stop.configure(state = DISABLED)
        #button_play.configure(state = NORMAL)

def button_back_Click():
    root.destroy()

def button_next_Click():
    root.destroy()

def button_quit_Click():
    root.destroy()

def maximise ():
    global window_width
    global window_height
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    window_width = w * 0.6
    window_height = h * 0.6
    left_blank = (w - window_width) / 2
    top_blank = (h - window_height) / 2
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, left_blank, top_blank))


##################
#                #
#      GUI       #
#                #
##################
root = Tk()

script_list = read_file(SCRIPT_FILE)

###############################################
#      constants for controlling layout       #
###############################################
button_width = 8

button_padx = "2m"
button_pady = "1m"

buttons_frame_padx =  "3m"
buttons_frame_pady =  "2m"       
buttons_frame_ipadx = "3m"
buttons_frame_ipady = "1m"

##############################
#      set window size       #
##############################
maximise()

### Our topmost frame is called myContainer1
myContainer1 = Frame(root)
myContainer1.pack()

############################
#      message frame       #
############################
message_frame = Frame(myContainer1) ###
message_frame.pack(side = TOP, expand = NO,  padx = 10, pady = 5, ipadx = 5, ipady = 5)
        
myMessage = "This is a recording programme !\n"
Label(message_frame, text = myMessage, justify = LEFT).pack(side = TOP, anchor = W)

#########################
#      text frame       #
#########################
text_frame_height = int(0.5 * window_height)
text_frame_width = int(0.9 * window_width)

text_frame = Frame(myContainer1, borderwidth = 2,  relief = RIDGE, height = text_frame_height, width = text_frame_width, background = "white")
text_frame.pack(side = TOP, fill = BOTH, expand = YES)
text_frame.pack_propagate(0)    # enable size edit

script_line = StringVar()
script_line.set(script_list[0])

# use "wraplength" option to set auto warping
script_text = Label(text_frame, textvariable = script_line, font = ("Helvetica", 50), justify = LEFT, height = text_frame_height, width = text_frame_width, wraplength = text_frame_width)
script_text.pack()

###########################
#      button frame       #
###########################
buttons_frame = Frame(myContainer1)
buttons_frame.pack(side = TOP, ipadx = buttons_frame_ipadx, ipady = buttons_frame_ipady, padx = buttons_frame_padx, pady = buttons_frame_pady)                  
        
# back button
button_back = Button(buttons_frame, command = button_back_Click)
button_back.configure(text = "Back", font = ("Helvetica", 15))
button_back.configure(width = button_width, padx = button_padx, pady = button_pady)
button_back.pack(side = LEFT)

# next button
button_next = Button(buttons_frame, command = button_next_Click)
button_next.configure(text = "Next", font = ("Helvetica", 15))
button_next.configure(width = button_width, padx = button_padx, pady = button_pady)
button_next.pack(side = LEFT)

# record button
button_record = Button(buttons_frame, command = button_record_Click)
button_record.configure(text = "Record", font = ("Helvetica", 15))
button_record.configure(width = button_width, padx = button_padx, pady = button_pady)
button_record.pack(side = LEFT)

# stop button
button_stop = Button(buttons_frame, command = button_stop_Click)
button_stop.configure(text = "Stop", font = ("Helvetica", 15))  
button_stop.configure(width = button_width, padx = button_padx, pady = button_pady)
button_stop.configure(state = DISABLED) 
button_stop.pack(side = LEFT)
        
# play button
button_play = Button(buttons_frame, command = button_play_Click)
button_play.configure(text = "Play", font = ("Helvetica", 15))  
button_play.configure(width = button_width, padx = button_padx, pady = button_pady)
button_play.configure(state = DISABLED) 
button_play.pack(side = LEFT)

# quit button
button_quit = Button(buttons_frame, command = button_quit_Click)
button_quit.configure(text = "Quit", font = ("Helvetica", 15))
button_quit.configure(width = button_width, padx = button_padx, pady = button_pady)
button_quit.pack(side = LEFT)

#########################
#      foot frame       #
#########################
foot_frame = Frame(myContainer1) ###
foot_frame.pack(side = BOTTOM, fill = BOTH, expand = YES)
        
### author_frame 
author_frame = Frame(foot_frame, borderwidth = 0,  relief=  RIDGE, width = 200) 
author_frame.pack(side = LEFT, fill = BOTH, expand = YES)  
myMessage_author = "Author: Mengxue Cao"
Label(author_frame, text = myMessage_author, justify = LEFT).pack(side = LEFT, anchor = W)

### version_frame 
version_frame = Frame(foot_frame, borderwidth = 0,  relief = RIDGE, width = 200)
version_frame.pack(side = RIGHT,fill = BOTH, expand = YES)
myMessage_version = "Version: 0.1"
Label(version_frame, text = myMessage_version, justify = RIGHT).pack(side = RIGHT, anchor = W)


##################
#                #
#      MAIN      #
#                #
##################
def main():
    global state
    global save_buffer

    state = 0
    save_buffer = []    

    root.wm_title('PyRecorder')
    root.mainloop()
      
if __name__ == "__main__":
    main()
