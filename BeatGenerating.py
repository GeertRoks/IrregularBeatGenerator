import random
import time


#Kick Generator
def KickGen(amountOfSixteenths):
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
def SnareGen(kseq, amountOfSixteenths):
    seq = []
    for i in range(0, 3):       #generate 3 snares
        while True:
            rndnote = random.randint(0, (amountOfSixteenths - 1))
            if rndnote in kseq or rndnote in seq:       #check if already Kick or snare is played
                continue
            else:
                break
        seq.append(rndnote)
    seq = sorted(seq)
    return seq


#HiHat Generator
def HiHatGen(amountOfSixteenths):
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
