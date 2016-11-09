# README #

### BauTek Mini Pinball RGBSet and RGBSet Designer ###
(March 2016)

Includes RGBSet, an application that sets the cabinet RGB and Philips Hue lights to match the selected table and the RGBSet Designer to help you create lighting schemes. 


### Setup and Configuration ###

RGBSet has only been tested on Windows systems but should be adaptable enough to work on Linux or OSX with minor revisions.

The RGBSet.ini file contains all your system settings and the lighting profiles for your tables. As of March 2016 it's loaded with profiles for all of the currently available Zen Pinball tables.

1. Install Python 2.7 on your system and make sure the install directory is in your path list (the 2.7 installer should also associate .py files with python)
2. Edit the RGBSet.ini file so that the comport, hueip and huelights settings match your configuration. You can toggle either lighting feature by changing the hueenabled and logoenabled options.
3. Test your setup by running RGBSet.py -t <tablename> (ie. RGBSet.py -t EarthDefense). Your lights should react, otherwise RGBSet should respond with some troubleshooting messages.
4. Setup your launcher to trigger the RGBSet.py command when a table is launched and use RGBDesign.py to create your own custom profiles

### Usage ###

Set lights to match the active table (<tablename> as defined in RGBSet.ini)
*RGBSet.py -t <tablename>*

Start the RGBSet Designer
*RGBDesign.py*

### Future Plans ###

- Create a better interface for the RGBSet Designer to make tweaking light values easier
- Store the pre-execution cabinet RGB and Hue light values so the lights can be reset when the user quits the table
- Create a setup program that makes it easier to test the Arduino serial connections and choose the right Hue lights
- Add support for Hue light macros, enable things like light pulsing and gradient blends
- Integrate with the other cabinet controllers to enable light feedback during bumper hits





