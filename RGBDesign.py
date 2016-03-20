import serial
import sys
import getopt
import ConfigParser
import os
import time

config = ConfigParser.SafeConfigParser()
config.read('RGBSet.ini')
comPort = config.get('program', 'comport')
baud = config.getint('program', 'baud')
ser = serial.Serial(comPort, baud)

currentTable = ""
currentLogoRGB = ""
currentRoomRGB = ""
menuMessage = ""
changesPending = 0

if ser:
    print "Serial connection on "+comPort+" established."
    time.sleep(2)

while True:
    os.system('cls')
    print "BauTek RGBSet Designer, Main Menu\nA. Table Select\nB. Enter new logo RGB values\nC. Enter new room RGB values\nD. Save table changes\n\nQ. Quit\n"

    if currentTable == "":
        print "Current table: <no table selected>"
    else:
        print "Current table: "+currentTable

    if currentLogoRGB == "":
        print "Current Logo RGB: <no RGB data>"
    else:
        print "Current Logo RGB: "+currentLogoRGB

    if currentRoomRGB == "":
        print "Current Room RGB: <no RGB data>"
    else:
        print "Current Room RGB: "+currentRoomRGB

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
                changesPending = 0;

        if changesPending == 0:    
            tableInput = raw_input("Enter the table name |> ")
            if config.has_section(tableInput):
                currentTable = tableInput
                currentLogoRGB = config.get(currentTable, 'logocolor')
                currentRoomRGB = config.get(currentTable, 'roomcolor')
                ser.write(currentLogoRGB.encode('UTF-8'))

            else:
                junk = raw_input("Invalid table entered, try again or verify the integrity of the configuration file. Enter to continue...")
                menuMessage = "Invalid table selected "
                                 
    elif mainMenuSelect == "B" or mainMenuSelect == "b":
        print "\n"
        if currentTable == "":
            junk = raw_input("No table selected, select a table first. Enter to continue...")
        else:
            currentLogoRGB = raw_input("Enter comma-separated RGB values (eg. 255,255,255) |> ")
            ser.write(currentLogoRGB.encode('UTF-8'))
            menuMessage = "Logo "+currentLogoRGB+" set "
            changesPending = 1

    elif mainMenuSelect == "C" or mainMenuSelect == "c":
        print "\n"
        if currentTable == "":
            junk = raw_input("No table selected, select a table first. Enter to continue...")
        else:
            currentRoomRGB = raw_input("Enter comma-separated RGB values (eg. 255,255,255) |> ")
            menuMessage = "Room "+currentRoomRGB+" set "
            changesPending = 1

    elif mainMenuSelect == "D" or mainMenuSelect == "d":
        print "\n"
        if currentTable == "" or currentLogoRGB == "" or currentRoomRGB == "":
            junk = raw_input("Table or RGB selections are invalid, please complete all items. Enter to continue...")
        else:
            config.set(currentTable, 'logocolor', currentLogoRGB)
            config.set(currentTable, 'roomcolor', currentRoomRGB)
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
