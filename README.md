# _PyRecorder_

**_by Mengxue Cao_**

PyRecorder is a voice recorder written in Python. The audio module is based on [PyAudio](http://people.csail.mit.edu/hubert/pyaudio/).
The GUI is based on [Tkinter](https://wiki.python.org/moin/TkInter). The goal of this programme is to help phoneticians do easy recording.

## Features

1. Set recording parameters such as sampling rate, recording channels, bit rate etc.
2. Do series recording by reading in a prepared script file.
3. Play back recordings.
4. Jump between recording items.
5. Dynamically set the format of sound file name based on number of sentences to be recorded (require python 2.6 or higher).
	* if the number of sentences is in (0, 10), use 1.wav, 2.wav ...
	* if the number of sentences is in [10, 100), use 01.wav, 02.wav ...
	* if the number of sentences is in [100, 1000), use 001.wav, 002.wav ...
	* ...

## Usage

1. Prepare a file contains recording scripts. In the file, each line should only contain one sentence (or word). 
2. Run the code with "python PyRecorder.py".
3. Set parameters by clicking the "Setting" button.
4. Click "Record" to start recording, and click "Stop" to stop.
5. Click "Play" to play back.
6. Click "Back" and "Next" to navigate.

## Required dependencies

The code is written in Python 2. To run the programme, PyAudio and Tkinter are required.
* PyAudio provides Python bindings for PortAudio.
	* see [PyAudio](http://people.csail.mit.edu/hubert/pyaudio/) home page for installation guids and more information.
* Tkinter is Python's de-facto standard GUI package.
	* see [Tkinter](https://wiki.python.org/moin/TkInter) wiki page for more information.
	* also see a [Tkinter tutorial](http://effbot.org/tkinterbook/) from effbot.org.

## Compatibility

The programme is, by now, only tested under OS X EI Capitan (10.11.2) with python 2.7.11. The menu bar feature is specifically designed for OS X platform. However, with some small modifications, the code should be able to run on other platforms such as Linux and Windows, based on the cross-platform compabiity of python.


## Standalone app

If you donot have a runable python environment, or if you just donot want to install those required packages, a standalone OS X app (see [standalone_app](https://github.com/smilett/PyRecorder/tree/master/standalone_app)) is your good choice.

The app is built by "py2app". If you would like to biuld your own version of PyRecorder OS X app, please find more information on [py2app](https://pythonhosted.org/py2app/) homepage.
* NOTE: when building you app using "py2app", please set `'argv_emulation': False` in your "setup.py" file. Otherwise, your app would not appear at front when you open it.

## Known issues

When doing recording or playing, a warning will shown up in the command line, shown `the application is using the deprecated Carbon Component Manager for hosting Audio Units`. This is probably a problem of EI Capitan, but it does not affect the programme performance at the moment.

## History

see [Changelog](https://github.com/smilett/PyRecorder/blob/master/CHANGELOG.md) file.

## License

MIT license, see [LICENSE](https://github.com/smilett/PyRecorder/blob/master/LICENSE) file.