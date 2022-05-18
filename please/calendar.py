import os
from os.path import expanduser
import please

# from ics import Calendar

config_path = os.path.join(expanduser("~"), ".config", "please")
ics_file = [file for file in os.listdir(config_path) if file.endswith(".ics")]

if len(ics_file) != 1:
    print("Please make sure that there's only one '.ics' file in ~/.config/please")
    quit()

ics_file_name = ics_file[0]
print(ics_file_name)


def addcalendar(path: string):
    path
