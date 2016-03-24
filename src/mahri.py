#!/usr/bin/python

"""
Main file to run Mahri modules
"""

CONFIG_FILE = 'config/kghite_config.ini'

from ConfigParser import SafeConfigParser
import trackHeadTilt

# Import config variables
config = SafeConfigParser()
config.read(CONFIG_FILE)
camera = int(config.get('camera_settings', 'camera'))
rEyeFile = config.get('opencv_files', 'right_eye_path')
lEyeFile = config.get('opencv_files', 'left_eye_path')

print lEyeFile

if __name__ == "__main__":
	trackHeadTilt.run(camera, rEyeFile, lEyeFile)