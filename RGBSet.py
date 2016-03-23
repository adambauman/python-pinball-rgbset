import serial
import sys
import getopt
import ConfigParser
import os
import time
from hue import Hue  # python-hue library

myHue = Hue()
config = ConfigParser.SafeConfigParser()

def main(argv):
    config.read('RGBSet.ini')
    comPort = config.get('program', 'comport')
    baud = config.getint('program', 'baud')
    hueEnabled = config.getint('program', 'hueEnabled')
    logoEnabled = config.getint('program', 'logoEnabled')
    hueLightList = config.get('program', 'hueLights')
    hueIP = config.get('program', 'hueIP')

    tableName = ""
    logoColor = "128,10,0"

    if hueEnabled == 0 and logoEnabled == 0:
        print "Logo and Hue lighting disabled, closing RGBSet."
        quit()

    try:
        opts, args = getopt.getopt(argv, "h:t:")
    except getopt.GetoptError:
        print 'Sets the color of table and room lights. Loads color data from RGBSet.ini\n\nUsage: RGBSet.py -t <tablename>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Sets the color of table and room lights. Loads color data from RGBSet.ini\n\nUsage: RGBSet.py -t <tablename>'
            sys.exit()
        elif opt in "-t":
            tableName = arg

    if tableName:
        if config.has_section(tableName) and config.has_option(tableName, 'logocolor') and logoEnabled == 1:
            logoColor = config.get(tableName, 'logocolor')
            print "Opening connection on " + comPort

            try:
                ser = serial.Serial(comPort, baud)
                if ser:
                    print "Serial communication on " + comPort + " successful."
                    time.sleep(2)
            except:
                print "Serial communication on " + comPort + " failed."

            print "Sending "+logoColor
            encodedLogoColor = logoColor.encode(encoding='UTF-8')

            try:
                ser.write(encodedLogoColor)
            except:
                print "Serial communication error on " + comPort + "."
                quit()
        else:
            print "Configuration error, '" + tableName + "' can't be found in RGBSet.ini or logo lighting disabled."

        if config.has_section(tableName) and config.has_option(tableName, 'huebri') and config.has_option(tableName, 'huesat') and config.has_option(tableName, 'huehue') and hueEnabled == 1:
            hueBri = config.getint(tableName, 'huebri')
            hueSat = config.getint(tableName, 'huesat')
            hueHue = config.getint(tableName, 'huehue')

            myHue.station_ip = hueIP
            print "Connecting to your Hue hub..."
            print "Note: If this process hangs for over two minutes, hit CTRL+C and check the FAQ.\n"
            print "*** Press the hub's link button now! ***"
            myHue.get_state()
            hueLight = myHue.lights.get('l10')
            hueLight.set_state({"bri": hueBri, "sat": hueSat, "hue": hueHue})
        else:
            print "Configuration error, '" + tableName + "' can't be found in RGBSet.ini or Hue lighting disabled."

if __name__ == "__main__":
    main(sys.argv[1:])
