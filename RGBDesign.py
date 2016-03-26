#
#  BauTek Mini Pinball RGBSet
#  Sets the light parameters for cabinet LED and Philips Hue lights
#
#  3/2016 - Adam J. Bauman - adam@kungfutreachery.net
#

import serial # pyserial library
import ConfigParser
import os
import time

try:
    os.remove('hue.log')  # Flush the Hue log
except:
    print "Error clearing hue.log"

from hue import Hue  # python-hue library

myHue = Hue()
ser = serial.Serial()
config = ConfigParser.SafeConfigParser()

try:
    config.read('RGBSet.ini')
    hueEnabled = config.getint('program', 'hueEnabled')
    logoEnabled = config.getint('program', 'logoEnabled')
except:
    print "Error reading RGBset.ini. File is damaged or missing."
    quit()

# Pull in the general configuration
ser.port = config.get('program', 'comport')
ser.baudrate = config.getint('program', 'baud')
ser.timeout = 3
ser.setDTR(False)  # Disabling DTR should stop the Arduino from rebooting on connect

hueLightList = config.get('program', 'hueLights')
hueIP = config.get('program', 'hueIP')

currentTable = ""
currentLogoRGB = ""
currentLogoR = ""
currentLogoG = ""
currentLogoB = ""
currentHueBri = 255
currentHueSat = 255
currentHueHue = 0
menuMessage = ""
changesPending = 0

try:
    ser.open()
    print "Serial connection on " + comPort + " established.\n"
except:
    print "Error establishing serial connection."

myHue.station_ip = hueIP
print "Connecting to your Hue hub..."
print "Note: If this process hangs for over two minutes, hit CTRL+C and check the FAQ.\n"
print "*** Press the hub's link button now! ***"

try:
    myHue.get_state()
    # hueLight = myHue.lights.get('l10')
    hueLight = myHue.lights.get('l10')
except:
    print "Failed to communicate with the Hue hub, check IP and link status."


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
    if mainMenuSelect.lower() == "a":
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
                currentLogoRGBsplit = [x.strip() for x in currentLogoRGB.split(',')]
                currentLogoR = currentLogoRGBsplit[0]
                currentLogoG = currentLogoRGBsplit[1]
                currentLogoB = currentLogoRGBsplit[2]

                currentHueBri = config.getint(currentTable, 'hueBri')
                currentHueSat = config.getint(currentTable, 'hueSat')
                currentHueHue = config.getint(currentTable, 'hueHue')

                try:
                    ser.write(currentLogoRGB.encode('UTF-8'))
                except:
                    raw_input("Serial communication failed, press Enter to continue...")

                try:
                    hueLight.set_state({"bri": currentHueBri, "sat": currentHueSat, "hue": currentHueHue})
                except:
                    raw_input("Hue communication failed, press Enter to continue...")

            else:
                raw_input("Invalid entry, try again or check the configuration file. Enter to continue...")
                menuMessage = "Invalid table selected "

    # Logo entry
    elif mainMenuSelect.lower() == "b":
        print "\n"
        if currentTable == "":
            raw_input("No table selected, select a table first. Enter to continue...")
        else:
            print ""
            continueentry = 1
            while continueentry == 1:
                print "Enter Logo RGB values, blank entry will retain the existing value"
                print ""
                inputr = raw_input("Enter RED value   (0-255, current: %s) |> " % currentLogoR)
                inputg = raw_input("Enter GREEN value (0-255, current: %s) |> " % currentLogoG)
                inputb = raw_input("Enter BLUE value  (0-255, current: %s) |> " % currentLogoB)

                if inputr != "":
                    currentLogoR = inputr

                if inputg != "":
                    currentLogoG = inputg

                if inputb != "":
                    currentLogoB = inputb

                currentLogoRGB = "%s,%s,%s" % (currentLogoR, currentLogoG, currentLogoB)

                try:
                    ser.write(currentLogoRGB.encode('UTF-8'))
                except:
                    junk = raw_input("Serial communication failed, press Enter to continue...")

                print ""
                if raw_input("Are you happy with the color? Y to save, ENTER to try again |> ").lower() == "y":
                    continueentry = 0

            menuMessage = "Logo RGB set "
            changesPending = 1

    # Hue entry
    elif mainMenuSelect.lower() == "c":
        print ""
        if currentTable == "":
            raw_input("No table selected, select a table first. Enter to continue...")
        else:
            print ""
            continueentry = 1
            while continueentry == 1:
                print "Enter Hue parameters, blank entry will retain the existing value"
                inputbri = raw_input("Enter Brightness (0-255, current: %s) |>" % currentHueBri)
                inputsat = raw_input("Enter Saturation (0-255, current: %s) |> " % currentHueSat)
                inputhue = raw_input("Enter Hue        (0-65536, current: %s |> " % currentHueHue)

                if inputbri != "":
                    currentHueBri = int(inputbri)

                if inputsat != "":
                    currentHueSat = int(inputsat)

                if inputhue != "":
                    currentHueHue = int(inputhue)

                try:
                    hueLight.set_state({"bri": currentHueBri, "sat": currentHueSat, "hue": currentHueHue})
                except:
                    raw_input("Hue communication error, press ENTER to continue...")

                print ""
                if raw_input("Are you happy with the color? Y to save, ENTER to try again |> ").lower() == "y":
                    continueentry = 0

            menuMessage = "Hue params set "
            changesPending = 1

    # Save table changes
    elif mainMenuSelect.lower() == "d":
        print ""
        if currentTable == "" or currentLogoRGB == "":
            raw_input("Table or RGB selections are invalid, please complete all items. Enter to continue...")
        else:
            config.set(currentTable, 'logocolor', str(currentLogoRGB))
            config.set(currentTable, 'hueBri', str(currentHueBri))
            config.set(currentTable, 'hueSat', str(currentHueSat))
            config.set(currentTable, 'hueHue', str(currentHueHue))

            try:
                with open('RGBSet.ini', 'wb') as configfile:
                    config.write(configfile)
                menuMessage = "Save successful "
                changesPending = 0
            except:
                raw_input("Failed to write to RGBSet.ini! Press Enter to continue...")
                menuMessage = "Save failed "


    # Toggle logo
    elif mainMenuSelect.lower() == "e":
        print ""
        logoEnabled = 0
        config.set('program', 'logoenabled', str(logoEnabled))

        try:
            with open('RGBSet.ini', 'wb') as configfile:
                config.write(configfile)
            menuMessage = "Logo toggle set "
        except:
            raw_input("Failed to write to RGBSet.ini! Press Enter to continue...")
            menuMessage = "Save failed "

    # Toggle Hue
    elif mainMenuSelect.lower() == "f":
        print ""
        hueEnabled = 0
        config.set('program', 'hueenabled', str(hueEnabled))

        try:
            with open('RGBSet.ini', 'wb') as configfile:
                config.write(configfile)
            menuMessage = "Hue toggle set "
        except:
            raw_input("Failed to write to RGBSet.ini! Press Enter to continue...")
            menuMessage = "Save failed "

    # Set Hue light number
    elif mainMenuSelect.lower() == "g":
        print ""
        hueLightList = raw_input("Enter Hue light number: ")

        config.set('program', 'huelights', hueLightList)

        try:
            with open('RGBSet.ini', 'wb') as configfile:
                config.write(configfile)
            menuMessage = "Hue Light Number Set "
        except:
            raw_input("Failed to write to RGBSet.ini! Press Enter to continue...")
            menuMessage = "Save failed "

    # Set Hue hub IP
    elif mainMenuSelect.lower() == "h":
        print ""
        hueIP = raw_input("Enter Hue Hub IP: ")

        config.set('program', 'hueip', hueIP)

        try:
            with open('RGBSet.ini', 'wb') as configfile:
                config.write(configfile)
            menuMessage = "Hue IP Address Set "
        except:
            raw_input("Failed to write to RGBSet.ini! Press Enter to continue...")
            menuMessage = "Save failed "

    # Quit
    elif mainMenuSelect.lower() == "q":
        print ""
        if changesPending == 1:
            quitConfirm = raw_input("Unsaved settings will be lost, quit? [Y,N] |> ")
            if quitConfirm.lower() == "y":
                quit()
        else:
            quit()
