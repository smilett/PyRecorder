# _PyRecorder_

**_by Mengxue Cao_**

PyRecorder is a voice recorder written in Python. The audio module is based on [PyAudio] (http://people.csail.mit.edu/hubert/pyaudio/).
The GUI is based on [Tkinter] (https://wiki.python.org/moin/TkInter). The goal of this programme is to help phoneticians do easy redording.

## Features

1. Set recording parameters like sampling rate, recording channels, bit rate etc.
2. Do continuously recording by reading in a prepared script file.
3. Dynamically set the format of sound file name based on number of sentences to be recorded (require python 2.6 or higher).
	* if the number of sentences is in (0, 10), use 1.wav, 2.wav ...
	* if the number of sentences is in [10, 100), use 01.wav, 02.wav ...
	* if the number of sentences is in [100, 1000), use 001.wav, 002.wav ...
	* ...
4. Play back recordings.
5. Jump between recording items.

## Environment Requirements

To run the programme, PyAudio and Tkinter are required
* PyAudio provides Python bindings for PortAudio, the cross-platform audio I/O library.
	* see [PyAudio] (http://people.csail.mit.edu/hubert/pyaudio/) home page for installation guids and more information.
* Tkinter is Python's de-facto standard GUI (Graphical User Interface) package.
	* see [Tkinter] (https://wiki.python.org/moin/TkInter) wiki page for more information.

## Compatibility

The programme is, by now, only tested under OS X EI Capitan (10.11.2) with python 2.7.11.
However, the code should be able to run on other platforms such as Linux and Windows, based on the cross-platform compabiity of python.


## Usage

1. Prepare a file contains recording scripts. In the file, each line should only contain one sentences (or words). 
2. Run the code with "python PyRecorder.py".
3. Set parameters by clicking the "Setting" button.
4. Click "Record" to start recording, and click "Stop" to stop.
5. Click "Play" to play back.

## History

2015-12-10 version 1.0 published

## License

MIT license, see [LICENSE] (https://github.com/smilett/PyRecorder/blob/master/LICENSE)