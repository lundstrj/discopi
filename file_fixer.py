import glob
import sys
import os
import subprocess


folders = []
folders.append("/home/pi/Music/1Abba/")
folders.append("/home/pi/Music/2Disco70/")
folders.append("/home/pi/Music/3Slow/")
folders.append("/home/pi/Music/4Jack/")
folders.append("/home/pi/Music/5/")
folders.append("/home/pi/Music/6/")

for folder in folders:
    files = glob.glob("%s/*.mp3" % folder)
    for f in files:
        if "'" in f:
            print "renaming %s" % f,
            #raw_input("OK?")
            new_name = f.replace("'","")
            print "to %s" % new_name
            os.rename(f, new_name)
