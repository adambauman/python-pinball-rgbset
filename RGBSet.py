#
#  BauTek Mini Pinball RGBSet
#  Sets the light parameters for cabinet LED and Philips Hue lights
#
#  3/2016 - Adam J. Bauman - adam@kungfutreachery.net
#

import serial  # pyserial library
import sys
import getopt
import ConfigParser
# import time
import os

try:
    os.remove('hue.log')  # Flush the Hue log
except:
    print "Error clearing hue.log"

from hue import Hue  # python-hue library



myHue = Hue()
ser = serial.Serial()
config = ConfigParser.SafeConfigParser()

config.read('RGBSet.ini')

try:
    logoEnabled = config.getint('program', 'logoEnabled')
    hueEnabled = config.getint('program', 'hueEnabled')
except:
    print "Error reading RGBSet.ini. Configuration is missing or corrupt."
    quit()

ser.port = config.get('program', 'comport')
ser.baudrate = config.getint('program', 'baud')
ser.timeout = 3
ser.setDTR(False)  # Disabling DTR should stop the Arduino from rebooting on connect

hueLightList = config.get('program', 'hueLights')
myHue.station_ip = config.get('program', 'hueIP')


def main(argv):
    tablename = ""

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
            tablename = arg

    if tablename and config.has_section(tablename):
        if config.has_option(tablename, 'logocolor') and logoEnabled == 1:
            logocolor = config.get(tablename, 'logocolor')

            print "Opening serial connection..."
            try:
                ser.open()
                print "Serial communication successful, sending color command"
                #time.sleep(2)
                encodedlogocolor = logocolor.encode(encoding='UTF-8')
                ser.write(encodedlogocolor)
            except:
                print "Serial communication failed, parameters: %s" % ser
        else:
            print "Configuration error, '" + tablename + "' isn't configured in RGBSet.ini or logo lighting disabled."

        if config.has_option(tablename, 'huebri') and config.has_option(tablename, 'huesat') and config.has_option(tablename, 'huehue') and hueEnabled == 1:
            huebri = config.getint(tablename, 'huebri')
            huesat = config.getint(tablename, 'huesat')
            huehue = config.getint(tablename, 'huehue')

            print "Connecting to your Hue hub..."
            try:
                myHue.get_state()
                huelight = myHue.lights.get('l10')
                huelight.set_state({"bri": huebri, "sat": huesat, "hue": huehue})
            except:
                print "Hue communication error, check hub link status and IP address"
        else:
            print "Configuration error, '" + tablename + "' isn't configured in RGBSet.ini or Hue lighting disabled."
    elif tablename != "":
        print "Invalid table name specified, check RGBSet.ini"
    else:
        print "Sets the color of table and room lights. Loads color data from RGBSet.ini\n\nUsage: RGBSet.py -t <tablename>"


if __name__ == "__main__":
    main(sys.argv[1:])
