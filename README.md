# chordgen

For all you Arturia KeyLab Mark 1 users out there that can’t use the pad matrix to play chords here’s a partial solution. The only way to make use of the Chord Pads that I could find was with Analog Lab1. Subsequent versions dropped chord support so the pad keys became somewhat redundant. Annoyingly the KeyLab Mark2 versions apparently support one-finger-chords. So here’s a bit of python fun for Mark1 users to get some use out of those chord pads after all.

In fact the python code should work with any midi keyboard that has built in pads though you may have to figure out what midi messages the pad keys generate. Arturia Keylab makes decoding the pads easy with their Midi Control Centre that configures pad functions. The pads default to playing single notes across the scale so you don’t need to change anything. If you are using other control templates you need to restore the default pad functions for the python code to work.

The python code, chordgen.py provides one-finger-chords across the whole keyboard not just by pressing pads. In fact the pads are used to select the chord to play eg major, minor, augmented or diminished, triads, sevenths or ninths, etc.

Chordgen only supports one-finger-chords at present and you can’t mix single notes but its useful if you are just auditioning chords and progressions. You select chords from the pad matrix show below:
![Alt text](padmap.png?raw=true)
 
Currently only triads, sevenths and ninths are available with major, minor, augmented and diminished versions. I’ll be adding a couple of inversion options soon.

Chordgen.py is here. You need Python 2.7 or 3.X to execute. Install the pygame module to provide midi support from here https://pypi.org/project/pygame/.  Chordgen.py has only been tested in a Windows environment and you need to have Tobias Erichsen’s  loopMidi running in the background. Get loopMidi from here http://www.tobias-erichsen.de/wp-content/uploads/2020/01/loopMIDISetup_1_0_16_27.zip. Using loopMidi add a named port eg ‘MyMidi’.

Open a Windows command window, cd to where you have downloaded chordgen.py, and enter:

python chordgen.py

This will display all the midi ports available in your system eg:

Device ID: 0 MMSystem Microsoft MIDI Mapper 0 1 0

Device ID: 1 MMSystem Bome MIDI Translator 1 1 0 0

Device ID: 2 MMSystem KeyLab 49 1 0 0

Device ID: 3 MMSystem MyMidi 1 0 0

Device ID: 4 MMSystem Microsoft GS Wavetable Synth 0 1 0

Device ID: 5 MMSystem Bome MIDI Translator 1 0 1 0

Device ID: 6 MMSystem KeyLab 49 0 1 0

Device ID: 7 MMSystem MyMidi 0 1 0

Identify the Keylab name to be your midi input, in my case ID 2 ‘Keylab 49 1 0 0’. Identify  your loopMidi port for midi output, in my case ID 7 ‘MyMidi  0 1 0’. Note if the last element of the Device string is a ‘1’ then the midi port is already opened by another application.

Now rerun the python this time with arguments:

python chordgen.py –i "KeyLab 49" –o "MyMidi"

Just leave the python running in the background and open say a DAW and connect to a VST. Make sure the VST gets its midi input from MyMidi and you should hear major triads the first time you hit a key. Change chord type by hitting the relevant pad as shown in the map above.

The python code is of course extensible so feel free to modify.
