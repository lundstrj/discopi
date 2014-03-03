import pifacedigitalio
import sys
import time
import mpylayer
import glob
from random import choice

mp = mpylayer.MPlayerControl()
pifacedigitalio.init()
pifacedigital = pifacedigitalio.PiFaceDigital()

print "starting up discopi"
print "port value:", pifacedigital.input_port.value

def light_on():
    print "light_on"
    pifacedigital.leds[0].turn_on()

def light_off():
    print "light_off"
    pifacedigital.leds[0].turn_off()

def ball_on():
    pifacedigital.leds[1].turn_on()

def ball_off():
    pifacedigital.leds[1].turn_off()    

def self_test():
    print "self_test"
    light_on()
    ball_on()
    time.sleep(0.5)
    light_off()
    ball_off()
    print "self_OK"

def pick_song():
    print "picking a new song!"
    songs = glob.glob("/home/pi/Disco 80-90/*.mp3")
    song = choice(songs)
    return song

def main():
    print "main"
    self_test()
    playing = False
    paused = False
    percent_pos = 0
    count_down = 0
    count_up = 0
    count = 0
    while True:
        print "down", count_down
        print "up", count_up
        if count == 10:
            print "::::::::::"
            count = 0
        count += 1
        if pifacedigital.input_port.value == 1:
            print "\nHIT\n"
            if playing and count_down == 1 and count_up < 10:
                print "Next song?"
                song = pick_song()
                print song
                mp.loadfile(song)
                time.sleep(0.1)
                count_up = 0
                count_down = 0
                continue
            if not playing and not paused:
                print "will start playing!"
                song = pick_song()
                print song
                mp.loadfile(song)
                time.sleep(0.1)
                playing = True
                count_up = 0
                count_down = 0
            elif playing and not paused:
                print "will pause"
                mp.pause()
                playing = False
                paused = True
                time.sleep(0.1)
                count_up = 0
                count_down = 0
            elif not playing and paused:
                print "will unpause"
                mp.pause()
                playing = True
                paused = False
                time.sleep(0.1)
                count_up = 0
                count_down = 0
            count_down += 1

        if count_up > 10:
            count_up = 0
            count_down = 0
        if pifacedigital.input_port.value == 0 and count_down > 0:
            count_up+=1


        if playing and mp.percent_pos != None:
            percent_pos = mp.percent_pos
            #print "pos",percent_pos
        else:
            time.sleep(0.2)
        if playing and percent_pos > 98:
            print "::::::::"
            print mp.percent_pos
            print "::::::::"
            raw_input("check")
            song = pick_song()
            print song
            mp.loadfile(song)
            time.sleep(0.1)
#try:
main()
#except:
#    print "Something went terribly wrong"

