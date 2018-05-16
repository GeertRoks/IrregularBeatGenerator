import simpleaudio as sa
import time

Kick = sa.WaveObject.from_wave_file("Kick.wav")
Snare = sa.WaveObject.from_wave_file("Snare.wav")
Tom = sa.WaveObject.from_wave_file("Tom.wav")

Kick_list =  [1,0,0,0,1,1,0,0]      #Kick, snare and tom matrix
Snare_list = [0,0,1,0,0,0,1,0]      # 1 = play, 0 = silence
Tom_list =   [0,1,0,1,0,0,0,1]

bpm = input("Beats per Minute? --> ")   #Bpm input
bpm = int(bpm)
interval = 30/(bpm) #bpm conversion, interval for eight notes

t0 = time.time()    #save starting time for refrence
beat = 0
while True: #infinite loop, Ctrl-C to stop
    if time.time() - t0 >= interval: #current time - pervious time >= interval?
        t0 = time.time() #new reference time

        if Kick_list[beat%8] == 1:      #checking lists in modulo 8
            Kick.play()                 #if 1 then play
        if Snare_list[beat%8] == 1:
            Snare.play()
        if Tom_list[beat%8] == 1:
            Tom.play()

        beat += 1                       #beat count increased

    else:
        time.sleep(0.01)
