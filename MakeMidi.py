from midiutil.MidiFile import MIDIFile
from midiutil import MIDIFile
import math

def MakeMidi(name, amountOfSixteenths, sixteenInterval, bpm, beatsPerMeasure, beatUnit, Kick_seq, Snare_seq, HiHat_seq):

    track    = 0
    channel  = 9                                #used midi channel
    time     = 0                                 #set time, in beats
    duration = 0.25                  #set duration in beats, 0.25 -> .../16 time signature
    bpm      = bpm                               #set bpm
    velocity = 100                               #set velocity     # 0-127, as per the MIDI standard


    #create a track - defaults to format 2 - to enable addTimeSignature functionality
    MyMIDI = MIDIFile(2, adjust_origin = True)
    #set track, tempo and time
    MyMIDI.addTempo(track, time, bpm)

    #add timesig
    MyMIDI.addTimeSignature(track, 0, beatsPerMeasure, int(math.log(beatUnit, 2)), 24)

    Kick = Kick_seq.pop(0)
    Snare = Snare_seq.pop(0)
    HiHat = HiHat_seq.pop(0)
    #add bassdrum
    for i in range(0, amountOfSixteenths):
        if i == Kick:
            MyMIDI.addNote(track, channel, 35, (time + i) * duration, duration, velocity)
            if Kick_seq:
                Kick = Kick_seq.pop(0)
        #add snare
        if i == Snare:
            MyMIDI.addNote(track, channel, 38, (time + i) * duration, duration, velocity)
            if Snare_seq:
                Snare = Snare_seq.pop(0)
        #add HiHat
        if i == HiHat:
            MyMIDI.addNote( track, channel, 42, (time + i) * duration, duration, velocity)
            if HiHat_seq:
                HiHat = HiHat_seq.pop(0)


    #write to MIDIfile
    with open("CreatedMidiFiles/" + name + ".mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
