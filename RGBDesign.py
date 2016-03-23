import serial # pyserial library
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
try:
    ser = serial.Serial(comPort, baud)
except:
    print "Error establishing serial connect on "+comPort
    ser = "failed"

if ser != "failed":
    print "Serial connection on "+comPort+" established.\n"
    time.sleep(2)

myHue.station_ip = hueIP
print "Connecting to your Hue hub..."
print "Note: If this process hangs for over two minutes, hit CTRL+C and check the FAQ.\n"
print "*** Press the hub's link button now! ***"
myHue.get_state()
hueLight = myHue.lights.get('l10')

while True:
    os.system('cls')
    print "BauTek RGBSet Designer, Main Menu"
    print ""
    print "A. Table Select"
    print "B. Enter new logo RGB values"
    print "C. Enter new Hue lighting values"
    print "D. Save table changes"
    print ""
    print "E. Toggle Logo Lighting"
    print "F. Toggle Hue Lighting"
    print "G. Select Hue Light Number"
    print "H. Set Hue Hub IP Address"
    print ""
    print "Q. Quit"
    print ""

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

    print ""

    if logoEnabled == 1:
        print "(Global) Logo Lighting: Enabled"
    else:
        print "(Global) Logo Lighting: Disabled"

    if hueEnabled == 1:
        print "(Global) Hue Lighting: Enabled"
    else:
        print "(Global) Hue Lighting: Disabled"

    if hueIP == "":
        print "(Global) Hue Hub IP Address: <not set>"
    else:
        print "(Global) Hue Hub IP Address: " + hueIP

    if changesPending == 1:
        menuMessage += "[Unsaved Changes] "

    mainMenuSelect = raw_input("\n"+menuMessage+"|> ")
    menuMessage = ""

    # Table select
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

                try:
                    ser.write(currentLogoRGB.encode('UTF-8'))
                except:
                    junk = raw_input("Serial communication failed, press Enter to continue...")

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

            try:
                ser.write(currentLogoRGB.encode('UTF-8'))
            except:
                junk = raw_input("Serial communication failed, press Enter to continue...")

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

    # Save table changes
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

    # Toggle logo
    elif mainMenuSelect == "E" or mainMenuSelect == "e":
        print "\n"
        logoEnabled = 0
        config.set('program', 'logoenabled', str(logoEnabled))

        with open('RGBSet.ini', 'wb') as configfile:
            config.write(configfile)

        menuMessage = "Logo Toggle Set "

    # Toggle Hue
    elif mainMenuSelect == "F" or mainMenuSelect == "f":
        print "\n"
        hueEnabled = 0
        config.set('program', 'hueenabled', str(hueEnabled))

        with open('RGBSet.ini', 'wb') as configfile:
            config.write(configfile)

        menuMessage = "Hue Toggle Set "

    # Set Hue light number
    elif mainMenuSelect == "G" or mainMenuSelect == "g":
        print "\n"
        hueLightList = raw_input("Enter Hue light number (easy to find in the Hue app): ")

        config.set('program', 'huelights', hueLightList)

        with open('RGBSet.ini', 'wb') as configfile:
            config.write(configfile)

        menuMessage = "Hue Light Number Set "

    # Set Hue hub IP
    elif mainMenuSelect == "H" or mainMenuSelect == "h":
        print "\n"
        hueIP = raw_input("Enter Hue Hub IP: ")

        config.set('program', 'hueip', hueIP)

        with open('RGBSet.ini', 'wb') as configfile:
            config.write(configfile)

        menuMessage = "Hue IP Address Set "

    # Quit
    elif mainMenuSelect == "Q" or mainMenuSelect == "q":
        print "\n"
        if changesPending == 1:
            quitConfirm = raw_input("Unsaved settings will be lost, quit? [Y,N] |> ")
            if quitConfirm == "Y" or quitConfirm == "y":
                quit()
        else:
            quit()
