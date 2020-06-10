# chordgen.py 09-06-20 1.0
# if you modify/republish code give a shout-out for the site:
# https://synthagora.blogspot.com/

import pygame.midi
import time, sys, argparse

def findMidiDevice(name, input):
    # return ID of midi device matching name for input (input=true) or output (input=false)
    
    for n in range(pygame.midi.get_count()):
        info = pygame.midi.get_device_info(n)
        if name in info:
            # info ('MMSystem', 'KeyLab 49', 1, 0, 0)
            # check if open
            if info[4] == 0:
                if input:
                    if info[2] == 1:
                        print ('Found Midi input device ' + name + ' ID: ' + str(n))
                        return n
                else:
                    if info[3] == 1:
                        print ('Found Midi output device ' + name + ' ID: ' + str(n))
                        return n
            else:
                print ('Midi device ' + name + ' already open')
                return -1
    print ('Midi device ' + name + ' not found')
    return -1
    
def getMidiDevices():
    # display info for all devices eg ('MMSystem', 'KeyLab 49', 1, 0, 0)
    
    for n in range(pygame.midi.get_count()):
        info = pygame.midi.get_device_info(n)
        device_line = 'Device ID: ' + str(n) + ' '
        for item in info:
            device_line += str(item) + ' '
        print(device_line)

def playChord(event, device, notes, note_number, velocity):
    # play chord if event = note_on (144), note off (128)

    for note in notes:
        if event == 144:
            device.note_on(note_number + note, velocity)

        if event == 128:
            device.note_off(note_number + note, velocity)

def genChord(chordtype):
    # generate chord notes
    
    chordnames = ['Major Triad','Minor Triad','Augmented Triad','Diminished Triad',
                    'Major Seventh','Minor Seventh','Augmented Seventh','Diminished Seventh',
                    'Major Ninth','Minor Ninth','Augmented Ninth','Diminished Ninth']
    print ('Chord type: ' + chordnames[chordtype])
    
    chords = [[0,4,7],[0,3,7],[0,4,8],[0,3,6],
                [0,4,7,11],[0,3,7,10],[0,4,8,12],[0,3,6,9],
                [0,4,7,11,14],[0,3,7,10,14],[0,4,8,10,14],[0,3,6,11,14]]
    return chords[chordtype]
    
def readInput(input_device, output_device):
    # read midi loop Ctrl-C to exit
    
    chordtype = 0
    notes = genChord(chordtype)
    
    output_device.set_instrument(0)
    try:
        while True:
            if input_device.poll():
                event = input_device.read(1)[0]
                # [[[144, 24, 120, 0], 1321]]
                # noteon, note, velocity
                data = event[0]
                timestamp = event[1]
                note_number = data[1]
                velocity = data[2]
                midievent = data[0] & 0xF0
                midichannel = data[0] & 0x0F
                #print ('Event: ' + str(midievent) + ' Channel: ' + str(midichannel))
                # counts channels from 0 so channel10 is 9
                if midichannel == 0:
                    playChord(midievent, output_device, notes, note_number, velocity)

                if midichannel == 9:     
                    # default keylab pad channel 10; pads default to single notes C1 upwards
                    if midievent == 144:
                         chordtype = note_number % 12
                         notes = genChord(chordtype)

    except KeyboardInterrupt:
        input_device.close()
        output_device.close()
        print ('Chordgen terminated')

pygame.midi.init()

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input", help="name of midi input device - use quotes if name has spaces")
parser.add_argument("-o","--output", help="name of midi output device - use quotes if name has spaces")
args = parser.parse_args()

if not args.input and not args.output:
    getMidiDevices()
    sys.exit()

if not args.input:
    print ('No input device specified')
    sys.exit()

if not args.output:
    print ('No output device specified')
    sys.exit()

input_device = findMidiDevice(args.input, True)
if input_device < 0:
    sys.exit()
output_device = findMidiDevice(args.output, False)
if output_device < 0:
    sys.exit()

my_input = pygame.midi.Input(input_device)     # keyboard ID
my_output = pygame.midi.Output(output_device)   # loopMidi ID

print ('Chordgen running (Ctrl-C to exit)')

readInput(my_input, my_output)  # loop Ctrl-C to exit
