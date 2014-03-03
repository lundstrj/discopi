def general_system_update():
    # sudo apt-get update 
    # sudo apt-get upgrade 
    # apt-get has a -y option
    pass

def update_discopi():
    pass

def check_network():
    # sudo ifconfig eht0
    # parse output
    pass

def reconnect_network():
    # sudo ifconfig eht0 down
    # sudo ifconfig eth0 up
    # sudo dhclient eth0
    # sudo ifconfig eht0
    # parse output
    pass

def enable_spi():
    # sudo apt-get install raspi-config
    # sudo raspi-config
    # apt-get -y install [packagename]


    # sudo modprobe spi-bcm2708

    #/etc/modprobe.d/raspi-blacklist.conf
    # comment out blacklist spi-bcm2708 from ^^^


    # create /etc/udev/rules.d/50-spi.rules
    # and add: KERNEL=="spidev*", GROUP="spi", MODE="0660"
    # groupadd spi
    # gpasswd -a pi spi
    pass

def install_piface():
    # sudo apt-get install python{,3}-pifacedigitalio
    pass

def install_pip():
    # sudo apt-get install python-pip
    pass