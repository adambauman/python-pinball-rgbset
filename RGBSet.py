import serial
import sys
import getopt
import ConfigParser
import os
import time


def main(argv):
    config = ConfigParser.SafeConfigParser()
    config.read('RGBSet.ini')
    comPort = config.get('program', 'comport')
    baud = config.getint('program', 'baud')
    ser = serial.Serial(comPort, baud)

    tableName = ""
    logoColor = "128,10,0"
    print "Opening connection on "+comPort
    time.sleep(2)

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
        if config.has_section(tableName) and config.has_option(tableName, 'logocolor'):
            logoColor = config.get(tableName, 'logocolor')
            print "Sending "+logoColor
        else:
            print "Configuration error, '" + tableName + "' can't be found in RGBSet.ini"

        encodedLogoColor = logoColor.encode(encoding='UTF-8')
        ser.write(encodedLogoColor)
        #print ser.readline()

if __name__ == "__main__":
    main(sys.argv[1:])
