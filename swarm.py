import pifacedigitalio
import sys
import subprocess
import time

pifacedigitalio.init()
pifacedigital = pifacedigitalio.PiFaceDigital()

print "starting up swarm"
print "port value:", pifacedigital.input_port.value

def play_sounds():
    print "play_sounds"
    play_sound("mplayer mario_here_we_go.wav")
    #play_sound("afplay mario_here_we_go.wav")
    play_sound("mplayer siren.wav")
    #play_sound("afplay siren.wav")

def play_sound(sound):
    cmd = sound
    process = subprocess.Popen(cmd, shell=True)
    out, err = process.communicate()
    errcode = process.returncode

def light_on():
    print "light_on"
    pifacedigital.leds[1].turn_on()

def light_off():
    print "light_off"
    pifacedigital.leds[1].turn_off()

def ball_on():
    pifacedigital.leds[0].turn_on()

def ball_off():
    pifacedigital.leds[0].turn_off()

def disco():
    light_on()
    ball_on()
    play_disco()
    light_off()
    ball_off()

def alarm_sequence():
    print "alarm_sequence"
    light_on()
    play_sounds()
    light_off()

def play_disco():
    print "play_disco"
    songs = ['101_the_trammps_-_disco_inferno-redrum.mp3', '102_anita_ward_-_ring_my_bell-redrum.mp3','103_chic_-_good_times-redrum.mp3']
    for song in songs:
        play_sound("mplayer %s" % song)
    

def self_test():
    print "self_test"
    light_on()
    time.sleep(0.5)
    light_off()
    play_sound("mplayer 1up.wav")
    print "self_OK"

def main():
    print "main"
    self_test()
    count = 0
    while True:
        if pifacedigital.input_port.value == 1 and count <= 2:
            play_sound("mplayer beep-7.wav")
            #play_sound("afplay beep-7.wav")
            time.sleep(1)
            count += 1
        elif pifacedigital.input_port.value == 1 and count == 3:
            play_sound("mplayer beep-8.wav")
            #play_sound("afplay beep-8.wav")
            time.sleep(1)
            count += 1
        elif pifacedigital.input_port.value == 1 and count == 4:
            alarm_sequence()
            count = 0
        elif pifacedigital.input_port.value == 0:
            count = 0
        elif pifacedigital.input_port.value == 2:
            # DISCO!
            disco()

    """
    q = Queue()
    t = Thread(target=input_loop, args = (q,))
    t.start()
    t2 = Thread(target=doer, args = (q,))
    t2.start()
    pifacedigital.input_port.value == 1
    """
try:
    main()
except:
    print "Something went terribly wrong"
    play_sound("mplayer dies.wav")

