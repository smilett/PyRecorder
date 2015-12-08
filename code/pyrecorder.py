#coding=utf-8  

from __future__ import division  
from pyaudio import PyAudio,paInt16
from Tkinter import *
import wave
import os

#####################
#                   #
#    Declaration    #
#                   #
#####################   
# define parameters
CHUNK = 1024        # frames per buffer
FORMAT = paInt16    # bit rate: 16-bit use "paInt16", 32-bit use "paInt32"
RATE = 44100        # sampling rate
CHANNELS = 1        # number of recording channels

WAV_PATH = "../wav/"    # saving path for wave files
SCRIPT_FILE = "../script/script"    # file of recording script


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
    l = s.split("\n")   # get each sentence and store them into a list

    return l


##################
#                #
#   RECORDING    #
#                #
##################

# record sound
def record_wav():
    global state, ave_buffer, stream_in
    
    # as long as the state is "recording", keep recording sounds
    if state == 1:                            
        string_audio_data = stream_in.read(CHUNK)
        save_buffer.append(string_audio_data) 

        # call the function once a millisecond
        # this enables Tkinter to handel other button-click events while recording
        root.after(1, record_wav)

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
    global state, data_out, stream_out, wav_out, wave_form, script_count, script_list

    # if reaches EOF, stop playing
    if len(data_out) == 0:
        state == 0  # change the state flag to "stopepd"
        echo_text.configure(text = "Stopped", bg = 'white', fg = 'black')
        stream_out.stop_stream()
        stream_out.close()
        wav_out.terminate()

        # update button states
        button_stop.configure(state = DISABLED)
        button_record.configure(state = NORMAL)
        if script_count > 0:
            button_back.configure(state = NORMAL)
        if script_count < len(script_list) - 1:
            button_next.configure(state = NORMAL)

    # else, play the sound, as long as the state is "playing"
    elif state == 2:
        stream_out.write(data_out)
        data_out = wave_form.readframes(CHUNK)

        # call the function once a millisecond
        # this enables Tkinter to handel other button-click events while playing
        root.after(1, play_wave)


#######################
#                     #
#    BUTTON CLICK     #
#                     #
#######################

def button_record_Click():
    global sampwidth, wav_in, stream_in, state

    state = 1   # change the state flag into "recording"

    # update button states
    button_stop.configure(state = NORMAL)
    button_play.configure(state = DISABLED)
    button_back.configure(state = DISABLED)
    button_next.configure(state = DISABLED)

    wav_in = PyAudio()
    stream_in = wav_in.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK) 
    sampwidth = wav_in.get_sample_size(FORMAT)
    echo_text.configure(text = "Recording...", bg = 'red', fg = 'white')
    record_wav()


def button_play_Click():
    global state, wav_out, stream_out, data_out, wave_form, wavefile, script_count, script_list

    state = 2   # change the state flag into "playing"

    # update button states
    button_stop.configure(state = NORMAL)
    button_record.configure(state = DISABLED)
    button_back.configure(state = DISABLED)
    button_next.configure(state = DISABLED)

    wav_out = PyAudio()
    wave_form = wave.open(WAV_PATH + wavefile, 'rb')
    stream_out = wav_out.open(format = wav_out.get_format_from_width(wave_form.getsampwidth()),
                channels = wave_form.getnchannels(),
                rate = wave_form.getframerate(),
                output = True)
    
    data_out = wave_form.readframes(CHUNK)
    echo_text.configure(text = "Playing...", bg = 'blue', fg = 'white')
    play_wave()
   
def button_stop_Click():
    global state, save_buffer, wav_in, wav_out, stream_in, stream_out, data_out, wavefile, script_count, script_list

    echo_text.configure(text = "Stopped", bg = 'white', fg = 'black')

    # stop from recording
    if state == 1:
        state = 0   # change the state flag into "stopped"
        save_wave_file(WAV_PATH + wavefile, save_buffer, sampwidth)

        # clean up
        save_buffer = []
        stream_in.stop_stream()
        stream_in.close()
        wav_in.terminate() 

        # update button states
        button_stop.configure(state = DISABLED)
        button_play.configure(state = NORMAL)
        button_record.configure(state = NORMAL)
        if script_count > 0:
            button_back.configure(state = NORMAL)
        if script_count < len(script_list) - 1:
            button_next.configure(state = NORMAL)

    # stop from playing
    elif state == 2:
        state = 0   # change the state flag into "stopped"

        # clean up
        stream_out.stop_stream()
        stream_out.close()
        wav_out.terminate() 
        data_out = []

        # update button states
        button_stop.configure(state = DISABLED)
        button_play.configure(state = NORMAL)
        button_record.configure(state = NORMAL)
        if script_count > 0:
            button_back.configure(state = NORMAL)
        if script_count < len(script_list) - 1:
            button_next.configure(state = NORMAL)


def button_back_Click():
    global script_count, script_line, wavefile, WAV_PATH

    if script_count > 1:        
        script_count = script_count - 1
        script_line.set(script_list[script_count])
        wavefile = str(script_count + 1) + '.wav'
        button_next.configure(state = NORMAL)

        # if file exists, enable play button
        if os.path.isfile(WAV_PATH + wavefile):
            button_play.configure(state = NORMAL)
        else:
            button_play.configure(state = DISABLED)

    elif script_count == 1:        
        script_count = script_count - 1
        script_line.set(script_list[script_count])
        wavefile = str(script_count + 1) + '.wav'

        # update button states
        button_back.configure(state = DISABLED)
        button_next.configure(state = NORMAL)

def button_next_Click():
    global script_count, script_line, wavefile, WAV_PATH

    if script_count < len(script_list) - 2:        
        script_count = script_count + 1
        script_line.set(script_list[script_count])
        wavefile = str(script_count + 1) + '.wav'
        button_back.configure(state = NORMAL)

        # if file exists, enable play button
        if os.path.isfile(WAV_PATH + wavefile):
            button_play.configure(state = NORMAL)
        else:
            button_play.configure(state = DISABLED)

    elif script_count == len(script_list) - 2:        
        script_count = script_count + 1
        script_line.set(script_list[script_count])
        wavefile = str(script_count + 1) + '.wav'

        # update button states
        button_back.configure(state = NORMAL)
        button_next.configure(state = DISABLED)

        # if file exists, enable play button
        if os.path.isfile(WAV_PATH + wavefile):
            button_play.configure(state = NORMAL)
        else:
            button_play.configure(state = DISABLED)

def button_quit_Click():
    root.destroy()

def maximise ():
    global window_width, window_height

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

# read in script file
script_list = read_file(SCRIPT_FILE)

# constants for controlling layout
button_width = 8

button_padx = "2m"
button_pady = "1m"

buttons_frame_padx =  "3m"
buttons_frame_pady =  "2m"       
buttons_frame_ipadx = "3m"
buttons_frame_ipady = "1m"


# set window size
maximise()

# create main frame
PyRecorder = Frame(root)
PyRecorder.pack(expand = YES, fill = BOTH)

#########################
#      text frame       #
#########################
text_frame_height = int(0.5 * window_height)
text_frame_width = int(0.9 * window_width)

text_frame = Frame(PyRecorder, borderwidth = 4,  relief = RIDGE, height = text_frame_height, width = text_frame_width, background = "white")
text_frame.pack(side = TOP, fill = BOTH, expand = YES, padx = 10, pady = 10, ipadx = 5, ipady = 5)
text_frame.pack_propagate(0)    # enable frame-size editing

script_line = StringVar()

# use "wraplength" option to set auto warping
script_text = Label(text_frame, textvariable = script_line, font = ("Helvetica", 50), justify = LEFT, height = text_frame_height, width = text_frame_width, wraplength = text_frame_width)
script_line.set(script_list[0])
script_text.pack()

###########################
#      button frame       #
###########################
buttons_frame = Frame(PyRecorder)
buttons_frame.pack(side = TOP, ipadx = buttons_frame_ipadx, ipady = buttons_frame_ipady, padx = buttons_frame_padx, pady = buttons_frame_pady)                  
        
# back button
button_back = Button(buttons_frame, command = button_back_Click)
button_back.configure(text = "Back", font = ("Helvetica", 15))
button_back.configure(width = button_width, padx = button_padx, pady = button_pady)
button_back.configure(state = DISABLED)
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
button_play.pack(side = LEFT)

# quit button
button_quit = Button(buttons_frame, command = button_quit_Click)
button_quit.configure(text = "Quit", font = ("Helvetica", 15))
button_quit.configure(width = button_width, padx = button_padx, pady = button_pady)
button_quit.pack(side = LEFT)

#########################
#      echo frame      #
#########################
echo_frame = Frame(PyRecorder) ###
echo_frame.pack(side = TOP, fill = BOTH, expand = YES)
echo_text = Label(echo_frame, text = "Stopped", font=("Helvetica", 50))
echo_text.pack(fill = BOTH, expand = YES)

#########################
#      foot frame       #
#########################
foot_frame = Frame(PyRecorder) ###
foot_frame.pack(side = BOTTOM, fill = BOTH, expand = YES)
        
### author_frame 
author_frame = Frame(foot_frame, borderwidth = 0,  relief=  RIDGE, width = 200) 
author_frame.pack(side = LEFT, fill = BOTH, expand = YES)  
myMessage_author = "Author: Mengxue Cao"
author = Label(author_frame, text = myMessage_author, justify = LEFT)
author.pack(side = BOTTOM, anchor = W)

### version_frame 
version_frame = Frame(foot_frame, borderwidth = 0,  relief = RIDGE, width = 200)
version_frame.pack(side = RIGHT,fill = BOTH, expand = YES)
myMessage_version = "Version: 0.1"
version = Label(version_frame, text = myMessage_version, justify = RIGHT)
version.pack(side = BOTTOM, anchor = E)

##################
#                #
#      MAIN      #
#                #
##################
def main():    
    global state, save_buffer, script_count, wavefile

    state = 0
    script_count = 0
    save_buffer = [] 
    wavefile = str(script_count + 1) + '.wav'

    # if file exists, enable play button
    if os.path.isfile(WAV_PATH + wavefile):
        button_play.configure(state = NORMAL)
    else:
        button_play.configure(state = DISABLED)

    root.wm_title('PyRecorder')
    root.mainloop()
      
if __name__ == "__main__":
    main()
