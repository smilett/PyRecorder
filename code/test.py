from Tkinter import *


#########################
# default parameters    #
#########################

root = Tk()

parameters = {'CHUNK':1024, 'FORMAT':16, 'RATE':44100, 'CHANNELS':1, 'WAV_PATH':'', 'SCRIPT_FILE':''}

MSG = 'Please enter seting parameters!'


def print_message():
	global parameters
	print parameters["WAV_PATH"]


b_login = Button(root, text='Log in')
b_login['command'] = lambda: Mbox(MSG, parameters)
b_login.pack()

b_loggedin = Button(root, text='parameters', command = print_message)
b_loggedin.pack()



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
        CHUNK = enteries[0].get()        # frames per buffer
        FORMAT = enteries[1].get()    # bit rate: 16-bit use "paInt16", 32-bit use "paInt32"
        RATE = enteries[2].get()        # sampling rate
        CHANNELS = enteries[3].get()        # number of recording channels
        WAV_PATH = enteries[4].get()   # saving path for wave files
        SCRIPT_FILE = enteries[5].get()    # file of recording script

        if CHUNK != '' and FORMAT != ''  and RATE != ''  and CHANNELS != ''  and WAV_PATH != ''  and SCRIPT_FILE != '' :
            parameters['CHUNK'] = CHUNK
            parameters['FORMAT'] = FORMAT
            parameters['RATE'] = RATE
            parameters['CHANNELS'] = CHANNELS
            parameters['WAV_PATH'] = WAV_PATH
            parameters['SCRIPT_FILE'] = SCRIPT_FILE

            self.top.destroy()

    def maximise(self):
        w, h = self.top.winfo_screenwidth(), self.top.winfo_screenheight()
        window_width = w * 0.3
        window_height = h * 0.4
        left_blank = (w - window_width) / 2
        top_blank = (h - window_height) / 2
        self.top.geometry("%dx%d+%d+%d" % (window_width, window_height, left_blank, top_blank))

Mbox.root = root

root.mainloop()