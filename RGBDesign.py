import serial
import sys
import getopt
import ConfigParser
import os

config = ConfigParser.SafeConfigParser()
config.read('RGBSet.ini')
comPort = config.get('program', 'comport')
baud = config.getint('program', 'baud')
ser = serial.Serial(comPort, baud)

while True:
    logoString = raw_input('Enter comma separated RGB values: ')
    ser.write(logoString.encode('UTF-8'))
    print(ser.readline())
