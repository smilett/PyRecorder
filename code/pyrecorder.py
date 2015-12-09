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
# default parameters
parameters = {'CHUNK':1024, 'FORMAT':16, 'RATE':44100, 'CHANNELS':1, 'WAV_PATH':'', 'SCRIPT_FILE':''}

Dialog_MSG = 'Please enter seting parameters!'


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
        echo_text.configure(text = "Stopped", bg = 'white', fg = 'black', font = ("Helvetica", 50))
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
    echo_text.configure(text = "Recording...", bg = 'red', fg = 'white', font = ("Helvetica", 50))
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
    echo_text.configure(text = "Playing...", bg = 'blue', fg = 'white', font = ("Helvetica", 50))
    play_wave()
   
def button_stop_Click():
    global state, save_buffer, wav_in, wav_out, stream_in, stream_out, data_out, wavefile, script_count, script_list

    echo_text.configure(text = "Stopped", bg = 'white', fg = 'black', font = ("Helvetica", 50))

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
    global script_count, script_list, script_line, wavefile, WAV_PATH

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
    global script_count, script_list, script_line, wavefile, WAV_PATH

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

def button_settings_Click():
    Mbox(Dialog_MSG, parameters)    

def button_about_Click():
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
#script_list = read_file(SCRIPT_FILE)

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
script_line.set('')
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
button_next.configure(state = DISABLED)
button_next.pack(side = LEFT)

# record button
button_record = Button(buttons_frame, command = button_record_Click)
button_record.configure(text = "Record", font = ("Helvetica", 15))
button_record.configure(width = button_width, padx = button_padx, pady = button_pady)
button_record.configure(state = DISABLED)
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
#      echo frame      #
#########################
welcome_message = "Please define the saving path and locate the recording script file\n by clicking the \"Settings\" button below!"
echo_frame = Frame(PyRecorder) ###
echo_frame.pack(side = TOP, fill = BOTH, expand = YES)
echo_text = Label(echo_frame, text = welcome_message, font=("Helvetica", 20), fg = 'blue')
echo_text.pack(fill = BOTH, expand = YES)

#########################
#      foot frame       #
#########################
foot_frame = Frame(PyRecorder) ###
foot_frame.pack(side = BOTTOM, fill = BOTH, expand = YES)
        
# settings button
button_settings = Button(foot_frame, command = button_settings_Click)
button_settings.configure(text = "Settings", font = ("Helvetica", 15))
button_settings.configure(width = button_width, padx = button_padx, pady = button_pady)
button_settings.pack(side = RIGHT)

# about button
button_about = Button(foot_frame, command = button_about_Click)
button_about.configure(text = "About", font = ("Helvetica", 15))
button_about.configure(width = button_width, padx = button_padx, pady = button_pady)
button_about.pack(side = RIGHT)


class Mbox(object):
    
    root = None

    def __init__(self, msg, parameters):
        """
        msg = <str> the message to be displayed
        dict_key = <sequence> (dictionary, key) to associate with user input
        (providing a sequence for dict_key creates an entry for user input)        
        """
        
        self.top = Toplevel(Mbox.root)
        self.maximise()
        self.top.wm_title('Settings')

        # disable inputs to the main window
        self.top.grab_set() 

        #########################
        #      text frame       #
        #########################
        text_frame = Frame(self.top)
        text_frame.pack(expand = YES, fill = BOTH)
        
        message = Label(text_frame, text = msg, font = ("Helvetica", 15), justify = LEFT)
        message.pack(padx = 4, pady = 4, expand = YES, fill = BOTH)

        ##########################
        #      entry frame       #
        ##########################
        entry_frame = Frame(self.top)
        entry_frame.pack(expand = YES, fill = X)        

        # CHUNK
        chunk_frame = Frame(entry_frame)
        chunk_frame.pack(expand = YES, fill = X) 
        
        text_CHUNK = Label(chunk_frame, text = "Frames per buffer:", font = ("Helvetica", 15), justify = LEFT)
        text_CHUNK.pack(side = LEFT, padx = 4, pady = 4)

        v_chunk = IntVar()
        radiobutton_chunk_1 = Radiobutton(chunk_frame, text = "1024", variable = v_chunk, value = 1024)
        radiobutton_chunk_1.pack(anchor = W, side = LEFT)

        radiobutton_chunk_2 = Radiobutton(chunk_frame, text = "2048", variable = v_chunk, value = 2048)
        radiobutton_chunk_2.pack(anchor = W, side = LEFT)
        v_chunk.set(parameters['CHUNK'])

        # FORMAT
        format_frame = Frame(entry_frame)
        format_frame.pack(expand = YES, fill = X)

        text_FORMAT = Label(format_frame, text = "Bit rate:", font = ("Helvetica", 15), justify = LEFT)
        text_FORMAT.pack(side = LEFT,padx = 4, pady = 4)

        v_format = IntVar()
        radiobutton_format_1 = Radiobutton(format_frame, text = "16-bit", variable = v_format, value = 16)
        radiobutton_format_1.pack(anchor = W, side = LEFT)

        radiobutton_format_2 = Radiobutton(format_frame, text = "32-bit", variable = v_format, value = 32)
        radiobutton_format_2.pack(anchor = W, side = LEFT)
        v_format.set(parameters['FORMAT'])

        # RATE
        rate_frame = Frame(entry_frame)
        rate_frame.pack(expand = YES, fill = X)

        text_RATE = Label(rate_frame, text = "Sampling rate:", font = ("Helvetica", 15), justify = LEFT)
        text_RATE.pack(side = LEFT,padx = 4, pady = 4)

        v_rate = IntVar()
        radiobutton_rate_1 = Radiobutton(rate_frame, text = "16 KHz", variable = v_rate, value = 16000)
        radiobutton_rate_1.pack(anchor = W, side = LEFT)

        radiobutton_rate_2 = Radiobutton(rate_frame, text = "22.05 KHz", variable = v_rate, value = 22050)
        radiobutton_rate_2.pack(anchor = W, side = LEFT)

        radiobutton_rate_3 = Radiobutton(rate_frame, text = "44.1 KHz", variable = v_rate, value = 44100)
        radiobutton_rate_3.pack(anchor = W, side = LEFT)
        v_rate.set(parameters['RATE'])

        # CHANNELS
        channels_frame = Frame(entry_frame)
        channels_frame.pack(expand = YES, fill = X)

        text_CHANNELS = Label(channels_frame, text = "Number of recording channels:", font = ("Helvetica", 15), justify = LEFT)
        text_CHANNELS.pack(side = LEFT,padx = 4, pady = 4)

        v_channels = IntVar()
        radiobutton_channels_1 = Radiobutton(channels_frame, text = "1", variable = v_channels, value = 1)
        radiobutton_channels_1.pack(anchor = W, side = LEFT)

        radiobutton_channels_2 = Radiobutton(channels_frame, text = "2", variable = v_channels, value = 2)
        radiobutton_channels_2.pack(anchor = W, side = LEFT)
        v_channels.set(parameters['CHANNELS'])

        # WAV_PATH
        wav_path_frame = Frame(entry_frame)
        wav_path_frame.pack(expand = YES, fill = X)

        text_WAV_PATH = Label(wav_path_frame, text = "Saving path:", font = ("Helvetica", 15), justify = LEFT)
        text_WAV_PATH.pack(side = LEFT,padx = 4, pady = 4)

        entry_WAV_PATH = Entry(wav_path_frame)
        entry_WAV_PATH.pack(side = LEFT, padx = 4, pady = 4, expand = YES, fill = BOTH)
        entry_WAV_PATH.insert(0, parameters['WAV_PATH'])

        # SCRIPT_FILE
        script_file_frame = Frame(entry_frame)
        script_file_frame.pack(expand = YES, fill = X)

        text_SCRIPT_FILE = Label(script_file_frame, text = "Recording script file:", font = ("Helvetica", 15), justify = LEFT)
        text_SCRIPT_FILE.pack(side = LEFT,padx = 4, pady = 4)

        entry_SCRIPT_FILE = Entry(script_file_frame)
        entry_SCRIPT_FILE.pack(side = LEFT, padx = 4, pady = 4, expand = YES, fill = BOTH)
        entry_SCRIPT_FILE.insert(0, parameters['SCRIPT_FILE'])

        enteries = [v_chunk, v_format, v_rate, v_channels, entry_WAV_PATH, entry_SCRIPT_FILE]

        ###########################
        #      button frame       #
        ###########################
        button_frame = Frame(self.top)
        button_frame.pack(expand = YES, fill = BOTH)

        b_submit = Button(button_frame, text = 'Submit')
        b_submit['command'] = lambda: self.submit(enteries)
        b_submit.pack(side = RIGHT)               

        b_cancel = Button(button_frame, text = 'Cancel')
        b_cancel['command'] = self.top.destroy
        b_cancel.pack(side = RIGHT)

    def submit(self, enteries):        
        p_CHUNK = enteries[0].get()        # frames per buffer
        p_FORMAT = enteries[1].get()    # bit rate: 16-bit use "paInt16", 32-bit use "paInt32"
        p_RATE = enteries[2].get()        # sampling rate
        p_CHANNELS = enteries[3].get()        # number of recording channels
        p_WAV_PATH = enteries[4].get()   # saving path for wave files
        p_SCRIPT_FILE = enteries[5].get()    # file of recording script

        if p_WAV_PATH == '':
            echo_text.configure(text = "Please set \"Saving path\"!\n", bg = 'white', fg = 'red', font = ("Helvetica", 20))
            self.top.destroy()

        elif p_SCRIPT_FILE == '':
            echo_text.configure(text = "Please set \"Recording script file\"!\n", bg = 'white', fg = 'red', font = ("Helvetica", 20))
            self.top.destroy()

        elif not os.path.exists(p_WAV_PATH):
            echo_text.configure(text = "Saving path does not exist!\n", bg = 'white', fg = 'red', font = ("Helvetica", 20))
            self.top.destroy()            
       
        elif not os.path.isfile(p_SCRIPT_FILE):
            echo_text.configure(text = "Recording script file does not exist!\n", bg = 'white', fg = 'red', font = ("Helvetica", 20))
            self.top.destroy()

        else:
            parameters['CHUNK'] = p_CHUNK
            parameters['FORMAT'] = p_FORMAT
            parameters['RATE'] = p_RATE
            parameters['CHANNELS'] = p_CHANNELS                    
            parameters['SCRIPT_FILE'] = p_SCRIPT_FILE
            
            if p_WAV_PATH[-1] != '/':
                parameters['WAV_PATH'] = p_WAV_PATH + '/'
            else:
                parameters['WAV_PATH'] = p_WAV_PATH

            self.top.destroy()

            echo_text.configure(text = "Stopped", bg = 'white', fg = 'black', font = ("Helvetica", 50))

            self.get_parameters(parameters)

            global wavefile, script_list

            wavefile = str(script_count + 1) + '.wav'

            # if file exists, enable play button
            if os.path.isfile(WAV_PATH + wavefile):
                button_play.configure(state = NORMAL)
            else:
                button_play.configure(state = DISABLED)

            
            script_list = read_file(SCRIPT_FILE)
            script_line.set(script_list[script_count])
            button_record.configure(state = NORMAL)
            button_next.configure(state = NORMAL)


    def get_parameters(self, parameters):
        global CHUNK, FORMAT, RATE, CHANNELS, WAV_PATH, SCRIPT_FILE

        CHUNK = parameters['CHUNK']        
        RATE = parameters['RATE']
        CHANNELS = parameters['CHANNELS']
        WAV_PATH = parameters['WAV_PATH']        
        SCRIPT_FILE = parameters['SCRIPT_FILE']

        if parameters['FORMAT'] == 16:
            FORMAT = paInt16
        elif parameters['FORMAT'] == 32:
            FORMAT = paInt32

    def maximise(self):
        w, h = self.top.winfo_screenwidth(), self.top.winfo_screenheight()
        window_width = w * 0.3
        window_height = h * 0.4
        left_blank = (w - window_width) / 2
        top_blank = (h - window_height) / 2
        self.top.geometry("%dx%d+%d+%d" % (window_width, window_height, left_blank, top_blank))


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

    root.wm_title('PyRecorder')
    Mbox.root = root
    root.mainloop()
      
if __name__ == "__main__":
    main()
