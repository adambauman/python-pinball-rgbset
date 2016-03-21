import serial
import sys
import getopt
import ConfigParser
import os
import time
from hue import Hue  # python-hue library

myHue = Hue()

config = ConfigParser.SafeConfigParser()
config.read('RGBSet.ini')

# Pull in the general configuration
comPort = config.get('program', 'comport')
baud = config.getint('program', 'baud')
hueEnabled = config.getint('program', 'hueEnabled')
logoEnabled = config.getint('program', 'logoEnabled')
hueLightList = config.get('program', 'hueLights')
hueIP = config.get('program', 'hueIP')

currentTable = ""
currentLogoRGB = ""
currentHueBri = 255
currentHueSat = 255
currentHueHue = 0
menuMessage = ""
changesPending = 0

# Begin communications
ser = serial.Serial(comPort, baud)
myHue.station_ip = hueIP
print "Connecting to your Hue hub...\n"
print "Note: If this process hangs for over two minutes, hit CTRL+C and check the FAQ.\n\n"
print "*** Press the hub's link button now! ***"
myHue.get_state()
hueLight = myHue.lights.get('l10')

if ser:
    print "Serial connection on "+comPort+" established."
    time.sleep(2)

while True:
    os.system('cls')
    print "BauTek RGBSet Designer, Main Menu\nA. Table Select\nB. Enter new logo RGB values\nC. Enter new Hue values\nD. Save table changes\n\nE. Toggle Logo Light\nF. Toggle Hue Light\n\nQ. Quit\n"

    if currentTable == "":
        print "Current table: <no table selected>"
    else:
        print "Current table: "+currentTable

    if currentLogoRGB == "":
        print "Current Logo RGB: <no RGB data>"
    else:
        print "Current Logo RGB: "+currentLogoRGB

    if currentTable == "":
        print "Current Hue Parameters: <no Hue data>"
    else:
        print "Current Hue Parameters: Bri= %s Sat= %s Hue= %s Light(s)= %s" % (currentHueBri, currentHueSat, currentHueHue, hueLightList)

    if logoEnabled == 1:
        print "(Global) Logo Lighting: Enabled"
    else:
        print "(Global) Logo Lighting: Disabled"

    if hueEnabled == 1:
        print "(Global) Hue Lighting: Enabled"
    else:
        print "(Global) Hue Lighting: Disabled"

    if changesPending == 1:
        menuMessage += "[Unsaved Changes] "

    mainMenuSelect = raw_input("\n"+menuMessage+"|> ")
    menuMessage = ""

    if mainMenuSelect == "A" or mainMenuSelect == "a":
        print "\n"
        tableChangeConfirm = ""
        if changesPending == 1:
            tableChangeConfirm = raw_input("There are unsaved changes to "+currentTable+", flush and switch tables? [Y,N] |> ")
            if tableChangeConfirm == "y" or tableChangeConfirm == "Y":
                changesPending = 0

        if changesPending == 0:    
            tableInput = raw_input("Enter the table name |> ")
            if config.has_section(tableInput):
                currentTable = tableInput
                currentLogoRGB = config.get(currentTable, 'logocolor')
                currentHueBri = config.getint(currentTable, 'hueBri')
                currentHueSat = config.getint(currentTable, 'hueSat')
                currentHueHue = config.getint(currentTable, 'hueHue')

                hueLight.set_state({"bri": currentHueBri, "sat": currentHueSat, "hue": currentHueHue})
                #hueLight.set_state({"bri": 128, "sat": 255, "hue": 40000})
                ser.write(currentLogoRGB.encode('UTF-8'))
            else:
                junk = raw_input("Invalid table entered, try again or verify the integrity of the configuration file. Enter to continue...")
                menuMessage = "Invalid table selected "

    # Logo entry
    elif mainMenuSelect == "B" or mainMenuSelect == "b":
        print "\n"
        if currentTable == "":
            junk = raw_input("No table selected, select a table first. Enter to continue...")
        else:
            currentLogoRGB = raw_input("Enter comma-separated RGB values (eg. 255,255,255) |> ")
            ser.write(currentLogoRGB.encode('UTF-8'))
            menuMessage = "Logo "+currentLogoRGB+" set "
            changesPending = 1

    # Hue entry
    elif mainMenuSelect == "C" or mainMenuSelect == "c":
        print "\n"
        if currentTable == "":
            junk = raw_input("No table selected, select a table first. Enter to continue...")
        else:
            currentHueBri = int(raw_input("Enter Hue Brightness (0-255) |> "))
            currentHueSat = int(raw_input("Enter Hue Saturation (0-255) |> "))
            currentHueHue = int(raw_input("Enter Hue Hue (0-65536) |> "))
            hueLight.set_state({"bri": currentHueBri, "sat": currentHueSat, "hue": currentHueHue})

            menuMessage = "Hue params set "
            changesPending = 1

    elif mainMenuSelect == "D" or mainMenuSelect == "d":
        print "\n"
        if currentTable == "" or currentLogoRGB == "":
            junk = raw_input("Table or RGB selections are invalid, please complete all items. Enter to continue...")
        else:
            config.set(currentTable, 'logocolor', str(currentLogoRGB))
            config.set(currentTable, 'hueBri', str(currentHueBri))
            config.set(currentTable, 'hueSat', str(currentHueSat))
            config.set(currentTable, 'hueHue', str(currentHueHue))

            with open('RGBSet.ini', 'wb') as configfile:
                config.write(configfile)

            menuMessage = "Save successful "
            changesPending = 0

    elif mainMenuSelect == "Q" or mainMenuSelect == "q":
        print "\n"
        if changesPending == 1:
            quitConfirm = raw_input("Unsaved settings will be lost, quit? [Y,N] |> ")
            if quitConfirm == "Y" or quitConfirm == "y":
                quit()
        else:
            quit()
