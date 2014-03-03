import pifacedigitalio
import sys
import time
import mpylayer
import glob
import subprocess
from random import choice
import RPi.GPIO as GPIO
import time
import os

mp = mpylayer.MPlayerControl()
pifacedigitalio.init()
pifacedigital = pifacedigitalio.PiFaceDigital()
skips = []

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
    play_sound("mplayer 1up.wav")
    print "self_OK"

def pick_song():
    print "picking a new song!"
    current_song = mp.filename
    suggestions = []
    if pifacedigital.input_pins[1].value:
        suggestions.append(choice(glob.glob("/home/pi/Music/1Abba/*.mp3")))
    if pifacedigital.input_pins[2].value:
        suggestions.append(choice(glob.glob("/home/pi/Music/2Disco70/*.mp3")))
    if pifacedigital.input_pins[3].value:
        suggestions.append(choice(glob.glob("/home/pi/Music/3Slow/*.mp3")))
    if pifacedigital.input_pins[4].value:
        suggestions.append(choice(glob.glob("/home/pi/Music/4Jack/*.mp3")))
    if pifacedigital.input_pins[5].value:
        suggestions.append(choice(glob.glob("/home/pi/Music/5/*.mp3")))
    # switch no 6 is for Spotify streaming (future feature)
    if pifacedigital.input_pins[6].value:
        suggestions.append(choice(glob.glob("/home/pi/Music/6/*.mp3")))
    # switch no 7 is for AirPlay support (future feature)
    #if pifacedigital.input_pins[7].value:
    #    suggestions.append(choice(glob.glob("/home/pi/Disco 80-90/*.mp3")))
    if suggestions == []:
        return False
    song = choice(suggestions)
    if song in skips:
        # try again
        return pick_song()
    # print "new song", song
    # print "old song", current_song
    if current_song in song:
        print "woups, almost picked the same song again =)"
        # try again
        return pick_song()
    # update current_song
    print song
    return song

def detect_press():
    time_out = 20
    counter = 0
    while pifacedigital.input_pins[0].value == 1:
        counter += 1
        time.sleep(0.01)
        if counter == time_out:
            break
    # print counter
    if counter < time_out:
        return True
    else:
        return False

def wait_short_enough():
    time_out = 20
    counter = 0
    while pifacedigital.input_pins[0].value == 0:
        counter += 1
        time.sleep(0.01)
        if counter == time_out:
            break
    # print counter
    if counter < time_out:
        return True
    else:
        return False

def get_skips():
    # read file
    # parse file
    # generate list of song names
    return []

def play_sound(sound):
    print "playing sound %s" % sound
    cmd = sound
    with open(os.devnull, "w") as fnull:
        process = subprocess.Popen(cmd, stdout = fnull, stderr = fnull, shell=True)
    out, err = process.communicate()
    errcode = process.returncode


def wait_button_let_go(shutdown = False):
    counter = 0
    while pifacedigital.input_pins[0].value == 1:
        time.sleep(0.01)
        counter += 1
        #print "wait:", counter
        if shutdown:
            if counter == 100:
                play_sound("mplayer beep-8.wav")
            elif counter == 200:
                play_sound("mplayer beep-8.wav")
            elif counter == 300:
                play_sound("mplayer beep-8.wav")
            elif counter == 400:
                play_sound("mplayer beep-7.wav")
            if counter > 500:
                return counter
    print "waited for ", counter
    return counter

def play_random_song():
    song = pick_song()
    if not song:
        print "no song picked, forgot to add folders?"
        play_sound("mplayer mario_hurry_up.wav")
        return False
    return play_song(song)

def play_song(song):
    mp.loadfile(song)
    return True


def main():
    print "main"
    self_test()
    skips = get_skips()
    started = False
    playing = False
    spinning = False
    percent_pos = 0
    passed1 = False
    passed2 = False
    passed3 = False
    while True:
        if not started:
            sys.stdout.write("Waiting to start.\r")
            sys.stdout.flush()
        if started and not spinning:
            pifacedigital.leds[0].turn_on()
            spinning = True
        if playing and mp.percent_pos != None:
            percent_pos = mp.percent_pos
        if playing: 
            if percent_pos != None:
                sys.stdout.write("Song progress: %d%%   \r" % (percent_pos) )
                sys.stdout.flush()
                if percent_pos == 25 and not passed1:
                    print "Song progress: %d" % (percent_pos)
                    passed1 = True
                if percent_pos == 50 and not passed2:
                    print "Song progress: %d" % (percent_pos)
                    passed2 = True
                if percent_pos == 75 and not passed3:
                    print "Song progress: %d" % (percent_pos)
                    passed3 = True
                if percent_pos > 97:
                    print "Song progress: %d" % (percent_pos)
                    print "end of song, time for a new one"
                    passed1 = False
                    passed2 = False
                    passed3 = False
                    if not play_random_song():
                        pass
                        #playing = False
                    time.sleep(0.5)

        if pifacedigital.input_pins[0].value == 1:
            if detect_press():
                # we have at least one press
                if wait_short_enough():
                    if detect_press():
                        print "two press"
                        if playing:
                            print "Pause"
                            playing = False
                            mp.pause()
                            time.sleep(0.1)
                        else:
                            print "Unpause"
                            playing = True
                            mp.pause()
                            time.sleep(0.1)
                        if pifacedigital.input_pins[7].value == 1:
                            play_sound("mplayer beep-8.wav")
                    else:
                        wait_button_let_go()
                        continue
                else:
                    print "one press"
                    if not started:
                        print "first time starting"
                        if not play_random_song():
                            print "not play_random_song() is True" 
                            print "NOT setting booleans True"
                            playing = False
                        else:
                            print "setting booleans True"
                            started = True
                            playing = True
                    else:
                        print "Next song"
                        if pifacedigital.input_pins[7].value == 1:
                            play_sound("mplayer beep-7.wav")
                        if not play_random_song():
                            print "Failed to get a new song to play, doing nothing"
                        elif not playing:
                            print "Automatic unpause"
                            time.sleep(0.2)
                            mp.pause()
                            time.sleep(0.2)
                            #mp.pause()
                            playing = True
                            #playing = False
            else:
                wait = wait_button_let_go(shutdown = True)
                if wait > 500:
                    print "Will shut down the system"
                    if playing:
                        mp.pause()
                        mp.quit()
                    play_sound("mplayer mario_dies.mp3")
                    pifacedigital.leds[0].turn_off()
                    pifacedigital.leds[1].turn_off()
                    os.system("sudo shutdown -h now")
            continue
main()
