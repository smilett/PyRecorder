#coding=utf-8  
  
from Tkinter import *  
import wave
import matplotlib.pyplot as plt  
import numpy as np  
  
def read_wave_data(file_path):  
    #open a wave file, and return a Wave_read object  
    f = wave.open(file_path,"rb")  
    #read the wave's format infomation,and return a tuple  
    params = f.getparams()  
    #get the info  
    nchannels, sampwidth, framerate, nframes = params[:4]  
    #Reads and returns nframes of audio, as a string of bytes.   
    str_data = f.readframes(nframes)  
    #close the stream  
    f.close()  
    #turn the wave's data to array  
    wave_data = np.fromstring(str_data, dtype = np.short)  
    #for the data is stereo,and format is LRLRLR...  
    #shape the array to n*2(-1 means fit the y coordinate)  
    wave_data.shape = -1, 2  
    #transpose the data  
    wave_data = wave_data.T  
    #calculate the time bar  
    time = np.arange(0, nframes) * (1.0/framerate)  
    return wave_data, time  
  
def main():  
    wave_data, time = read_wave_data("../wav/in/a_1.wav")     
    #draw the wave  
    plt.subplot(211)  
    plt.plot(time, wave_data[0])  
    plt.subplot(212)  
    plt.plot(time, wave_data[1], c = "g")  
    plt.show()  
  
if __name__ == "__main__":  
    main()  