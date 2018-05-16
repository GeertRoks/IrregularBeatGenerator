import time
import random
import _thread
import sys
import os
import simpleaudio as sa

import MakeMidi as midi

#TODO: Clean up code, add comments
"""
****************Read Me****************

To Marc and Ciska:

Deze code is niet perfect, maar het werkt!
De variabelen global doen is een tijdelijke oplossing, omdat
Classes me nog niet goed lukt. Daarom staan alle functies in
deze patch en niet meer in de andere losse patches.
Deze sampler heeft alleen maar MakeMidi.py nodig om te werken.


"""

global beatsPerMeasure, beatUnit, amountOfSixteenths, measureInterval, sixteenInterval, samples, events, copyEvents

#functions
def startUp():
    os.system('clear')
    print("Irregular Beat Generator (IBG)")
    print("Designed by: Geert Roks, 2017 \n")

def shutDown():
    os.system('clear')
    sys.exit()


def timeSig():  #input for Time signature
    global beatsPerMeasure, beatUnit, amountOfSixteenths
    while True:
        try:
            timesig = input("What time signature would you like to hear? --> ")
            timesig = timesig.strip().split("/") #timesig is now a list with [beats, count]

            beatUnit = int(timesig[1]) #Check Beat Unit
            if beatUnit != 2 and beatUnit != 4 and beatUnit != 8 and beatUnit != 16:
                print("Invalid beat unit. The beat unit has to be 2, 4, 8 or 16. Please enter one of the valid options. \n")
                continue

            beatsPerMeasure = int(timesig[0])  #Check Beats per meassure
            if beatsPerMeasure < 2 or  beatsPerMeasure > 12:
                print("Invalid beats per measure. The amount of beats per measure should be between 2 and 12.\n")
                continue
            elif beatsPerMeasure < 6 and beatUnit == 16:                        #expell short measures
                print("Shortest possible time signature is 6/16 or 3/8.\n")
            elif beatsPerMeasure == 2 and beatUnit == 8:
                print("Shortest possible time signature is 6/16 or 3/8.\n")
            elif beatsPerMeasure > 6 and beatUnit == 4:                         #expell long measures
                print("Longest possible time signature is 6/4 or 3/2.\n")
            elif beatsPerMeasure > 3 and beatUnit == 2:
                print("Longest possible time signature is 6/4 or 3/2.\n")
            else:
                amountOfSixteenths = beatsPerMeasure * int(16/beatUnit)
                break

        except:
            print("Invalid time signature. Please enter a valid time signature. For example: 7/8 \n" )

            continue
    return beatsPerMeasure, beatUnit, amountOfSixteenths



def BPM(): #input for bpm + calculation
    global beatsPerMeasure, beatUnit, measureInterval, sixteenInterval, bpm
    while True:
        bpm = input("How many beats per minute? --> ")
        if bpm.isdigit() and int(bpm) >= 40 and int(bpm) <= 300:
            bpm = int(bpm)
            beatInterval = (240/beatUnit)/(bpm) #bpm conversion, interval for beatUnit
            sixteenInterval = 15/(bpm) #interval of a sixteenth note
            measureInterval = beatsPerMeasure  * beatInterval #interval of a measure
            break
        else:
            print("Invalid response. Please enter a value between 40 and 300.\n")
    return measureInterval, sixteenInterval, bpm



def drumkitSelection():
    global samples
    while True:
        print("1. First selection")     #jazz kit
        print("2. Second selection")    #Rock kit
        print("3. Third selection")     #808
        print("4. Fourth Selection")    #African?
        drumkit = input("what kit would you like to play the beat on? --> ")
        if drumkit.isdigit() and int(drumkit) >= 1 and int(drumkit) <= 4:
            drumkit = int(drumkit)
            break
        else:
            print("Invalid response. Please enter a value between 1 and 4.\n")
            continue

    if drumkit == 1:
        samples = [ sa.WaveObject.from_wave_file("sounds/Kick.wav"),
                    sa.WaveObject.from_wave_file("sounds/Snare.wav"),
                    sa.WaveObject.from_wave_file("sounds/HiHat.wav"),    ]
    elif drumkit == 2:
        samples = [ sa.WaveObject.from_wave_file("sounds/Kick.wav"),
                    sa.WaveObject.from_wave_file("sounds/Snare.wav"),
                    sa.WaveObject.from_wave_file("sounds/HiHat.wav"),    ]
    elif drumkit == 3:
        samples = [ sa.WaveObject.from_wave_file("sounds/Kick.wav"),
                    sa.WaveObject.from_wave_file("sounds/Snare.wav"),
                    sa.WaveObject.from_wave_file("sounds/HiHat.wav"),    ]
    elif drumkit == 4:
        samples = [ sa.WaveObject.from_wave_file("sounds/Kick.wav"),
                    sa.WaveObject.from_wave_file("sounds/Snare.wav"),
                    sa.WaveObject.from_wave_file("sounds/Tom.wav"),      ]
    return samples



#Kick Generator
def KickGen():
    global amountOfSixteenths
    #choose how many kicks per measure
    rndchoice = random.randint(0, 8)
    x = 0
    if amountOfSixteenths <= 12:        #short measures
        seq = [0]           #mendatory kicks
        if rndchoice < 4:       #1/2 chance
            x = 1
        elif rndchoice >= 4 and rndchoice < 7:      #3/8 chance
            x = 2
        elif rndchoice == 7:    #1/8 chance
            x = 3
    elif amountOfSixteenths > 12 and amountOfSixteenths <= 20:  #middle measures
        seq = [0, 8]         #mendatory kicks
        if rndchoice < 4:   #1/2 chance
            x = 2
        elif rndchoice >= 4 and rndchoice < 7:      #3/8 chance
            x = 3
        elif rndchoice == 7:    #1/8 chance
            x = 4
    elif amountOfSixteenths > 20:       #long measures
        seq = [0, 8]        #mendatory kicks
        if rndchoice < 4:   #1/2 chance
            x = 3
        elif rndchoice >= 4 and rndchoice < 7:      #3/8 chance
            x = 4
        elif rndchoice == 7:    #1/8 chance
            x = 5
    x = x - len(seq)
    for i in range(0, x):
        while True:
            rndnote = random.randint(0, (amountOfSixteenths - 1))
            if rndnote in seq:
                continue
            else:
                break
        seq.append(rndnote)
        seq = sorted(seq)
    return seq


#Snare Generator
def SnareGen():
    global amountOfSixteenths, Kick_seq
    seq = []
    for i in range(0, 3):       #generate 3 snares
        while True:
            rndnote = random.randint(0, (amountOfSixteenths - 1))
            if rndnote in Kick_seq or rndnote in seq:       #check if already Kick or snare is played
                continue
            else:
                break
        seq.append(rndnote)
    seq = sorted(seq)
    return seq


#HiHat Generator
def HiHatGen():
    global amountOfSixteenths
    seq = []
    rndchoice = random.randint(0, 3)
    if rndchoice == 0:  #sixteenth not HiHat
        for i in range(amountOfSixteenths):
            seq.append(i)
    elif rndchoice == 1: #eight note HiHat
        for i in range(amountOfSixteenths):
            test = (i + 2) / 2
            if test.is_integer():
                seq.append(i)
    else:                #offbeat eight note HiHat
        for i in range(amountOfSixteenths):
            test = (i + 1) / 2
            if test.is_integer():
                seq.append(i)
    seq = sorted(seq)
    return seq

#Beat Generating
def GenerateBeat():
    global amountOfSixteenths, Kick_seq, Snare_seq, HiHat_seq
    #TODO: Improve snare algorithm
    Kick_seq  = KickGen()
    Snare_seq = SnareGen()
    HiHat_seq = HiHatGen()

    print("Kick Sequence:  " + str(Kick_seq))
    print("Snare Sequence: " + str(Snare_seq))
    print("Hihat Sequence: " + str(HiHat_seq))

    return Kick_seq, Snare_seq, HiHat_seq

#Transfer random beat to an Event list
def EventList():
    global sixteenInterval, Kick_seq, Snare_seq, HiHat_seq
    events = []

    #transform the sixteenthNoteSequece to an eventlist with time values
    for sixteenIndex in Kick_seq:
      events.append([sixteenIndex * sixteenInterval, 0])

    for sixteenIndex in Snare_seq:
      events.append([sixteenIndex * sixteenInterval, 1])

    for sixteenIndex in HiHat_seq:
      events.append([sixteenIndex * sixteenInterval, 2])
    events.sort() #sort events list so everything is in line to play at the right time

    return events

#PlaybackThread
def PlaybackThread():
    global events, samples, measureInterval, copyEvents

    #Playback init
    copyEvents = list(events) #events copy for repeating
    event = events.pop(0)
    t0 = time.time()    #save starting time for refrence

    while True:
        currentTime = time.time()
        if currentTime - t0 >= event[0]: #Check if it's time to play a sample
            if samples[event[1]] == 2:  #seperate play() for hihat, so polyphony is possible
                samples[2].play()
            else:                       #play() for Kick and Snare
                samples[event[1]].play()

            if events:  #if there are events left in the events list
                event = events.pop(0)
            else:   #list is empty, wait untill measure is done, then refill
                while True:
                    currentTime = time.time()
                    if currentTime - t0 >= measureInterval:
                        events = list(copyEvents)
                        event = events.pop(0)
                        t0 = time.time()
                        break
                    else:
                        time.sleep(0.01)
                        continue

        else:
            time.sleep(0.01)

#The Program

startUp()

#input questions
    #time signature
timeSig()

    #bpm
BPM()

    #drumkit TODO: Choose and download sample kits
drumkitSelection()


#Beat Generating
GenerateBeat()
events = EventList()

print("\nCommands: Gen, midi, bpm, timesig, quit.\n")
print("Gen      :   Generate new beat with current variables.")
print("midi     :   Export current beat to a midi file.")
print("bpm      :   Change bpm.")
print("timesig  :   Change time signature.")
print("quit     :   Exits program. \n")

#Input Thread during playback
#TODO: Solve the problem that gives a long silence or cluster of samples after bpm of time sig is changed
try:
   _thread.start_new_thread(PlaybackThread, ())
except:
   print("Error: unable to start thread \n")


# Loop checking for user input
while True:
    global copyEvents, measureInterval
    # Wait for keyboard input
    userInput = input("> ")

    # Splits input into a list, allows evaluating indiviual words
    userInput = userInput.split(" ")

    #Generate new
    if userInput[0].lower() == "gen":
        print("Freshly generated beat plays when current beat is done. ")
        GenerateBeat()
        copyEvents = EventList()

    #Make midi
    elif userInput[0].lower() == "midi":
        if len(userInput) == 2:
            name = userInput[1]
            midi.MakeMidi(name, amountOfSixteenths, sixteenInterval, bpm, beatsPerMeasure, beatUnit, Kick_seq, Snare_seq, HiHat_seq)
        else:
            print("Invalid name. Please write: 'midi <name>'. No spaces in name. ")

     # BPM
    elif userInput[0].lower() == "bpm":
        BPM()
        copyEvents = EventList()

    #timesig
    elif userInput[0].lower() == "timesig":
        timeSig()
        measureInterval = beatsPerMeasure  * (240/beatUnit)/(bpm)
        GenerateBeat()
        copyEvents = EventList()


    # Exit program
    elif userInput[0].lower() == "quit":
        shutDown()


    # Command not recognized
    else:
        print(" ".join(userInput),"not recognized, type help for an overview of all commands. \n")
