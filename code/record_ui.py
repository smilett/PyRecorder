#coding=utf-8  

from __future__ import division  
import numpy as np
from pyaudio import PyAudio,paInt16
from datetime import datetime
import matplotlib.pyplot as plt  
import wave
from Tkinter import *

  
#define of params
CHUNK = 1024
FORMAT = paInt16
RATE = 16000
CHANNELS = 1

#record time in terms of sampling points
RECORD_SECONDS = 3
RECORD_POINTS = int(RECORD_SECONDS * RATE / CHUNK)
  
def save_wave_file(filename, data, sampwidth):
    '''''save the date to the wav file'''
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(sampwidth)
    wf.setframerate(RATE)
    wf.writeframes("".join(data))
    wf.close()
  
def my_button(root,label_text,button_text,button_func):
    '''''''function of creat label and button'''
    #label details
    label = Label(root)
    label['text'] = label_text
    label.pack()
    #label details
    button = Button(root)
    button['text'] = button_text
    button['command'] = button_func
    button.pack()
      
def record_wave():
    #open the input of wave
    pa = PyAudio()

    stream = pa.open(format = FORMAT,
                     channels = CHANNELS,
                     rate = RATE,
                     input = True,
                     frames_per_buffer = CHUNK)
    
    print("* recording")

    save_buffer = []
    count = 0
    
    while count < RECORD_POINTS:
        #read CHUNK sampling data
        string_audio_data = stream.read(CHUNK)
        save_buffer.append(string_audio_data)        
        print '.'
        #plt.plot(count, float(string_audio_data))
        #plt.show()
        count += 1
    
    sampwidth = pa.get_sample_size(FORMAT)

    output_filename = datetime.now().strftime("../wav/out/%Y-%m-%d_%H_%M_%S")+".wav"
    save_wave_file(output_filename, save_buffer, sampwidth)

    save_buffer = []

    print output_filename, "saved"
  
def main():
    root = Tk()
    my_button(root,"Record a wave","clik to record",record_wave)
    root.mainloop()
      
if __name__ == "__main__":
    main()