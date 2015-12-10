# _PyRecorder_

* By Mengxue Cao

PyRecorder is a sound recorder written in Python. The audio module is based on PyAduio.
The GUI is based on Tkinter. The goal of this programme is to help phoneticians do easy redording.

## Features

* set recording parameters like sampling rate, recording channels, bit rate etc.
* able to do continuously recording by reading in a prepared script file.
* dynamically set the format of sound file name based on number of sentences to be recorded
	* if the number of sentences is in (0, 10), use 1.wav, 2.wav ...
	* if the number of sentences is in [10, 100), use 01.wav, 02.wav ...
	* if the number of sentences is in [100, 1000), use 001.wav, 002.wav ...
	* ...

## Environment Requirements

To run the programme, PyAudio and Tkinter are required
* PyAudio provides Python bindings for PortAudio, the cross-platform audio I/O library.
	* see [PyAudio] (http://people.csail.mit.edu/hubert/pyaudio/) home page for installation guids and more information.
* Tkinter is Python's de-facto standard GUI (Graphical User Interface) package.
	* see [Tkinter] (https://wiki.python.org/moin/TkInter) wiki page for more information.

## Usage

1. prepare a file contains recording scripts. In the file, each line should only contain one sentences (or words). 
2. run the code with "python PyRecorder.py".
3. set parameters by clicking the "Setting" button.
4. enjoy recording.

## History

version 1.0 published

## License

MIT license, see [LICENSE] (https://github.com/smilett/PyRecorder/blob/master/LICENSE)