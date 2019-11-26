# Security_System
Security system for home-usage with USB camera

packages used in this script: os, cv2, glob, argparse, time, datetime, concurrent.futures, simpleaudio, slack

This script works in two modes: 24/7 and "nightmode" available by using a argparse "-n" after the script name. 
Usage: just run the script with above pip packages installed like "python security_camera.py" or "python security_camera.py -n" for the night mode. 

This script is looking for a "difference" between pictures and when the difference is large enought(300 by default) it takes a photos. In 24/7 mode it sends the photos to slack channel with Slack api(needs to be set in Slack and API key able in ./bashrc file). With Night mode it only saves photos locally and plays a sound. You can change the sound just by replacing the .wav file in the directory.
