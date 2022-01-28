#! /usr/bin/env python
import subprocess, os,  sys, fileinput, datetime, argparse
from os import listdir
import csv,glob
from os.path import isfile, join
from datetime import datetime 
from fnmatch import fnmatch

def script(cmd): # normally return no 0 means error
    print ("[CMD]", cmd)
    try:
        ret = subprocess.call(cmd,  shell = True)
        if ret != 0:
            print("Failed: "+cmd)
    except:
        pass
    return ret

script_path = os.path.realpath(__file__)
script_path = os.path.dirname(script_path)
print(script_path)

data_folder = script_path+"/data"
csv_path = script_path+"/mscz-files.csv"

files_per_folder = 1000

downloaded_files = set()

pattern = "*.mscz"
for path, subdirs, files in os.walk(data_folder):
    for name in files:
        if fnmatch(name, pattern):
            fname = os.path.splitext(name)[0]
            downloaded_files.add(int(fname))

print(downloaded_files)

file_count = 0
current_folder_name = 0


with open(csv_path, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        line = row[0]
        if "ipfs" in line:
            items = line.split(",")
            name = items[0]
            current_folder = data_folder+"/"+str(current_folder_name)
            if not os.path.exists(current_folder):
                os.makedirs(current_folder)
            pattern = current_folder+"/*.mscz"
            # get file count in the folder
            current_files = len(glob.glob(pattern))
            if current_files>files_per_folder:
                current_folder_name = current_folder_name+1
            current_folder = data_folder+"/"+str(current_folder_name)
            if not os.path.exists(current_folder):
                os.makedirs(current_folder)
            os.chdir(current_folder)           

            if int(name) in downloaded_files:
                print("downloaded")
            else:
                print("new downloaded")
                #script("touch "+name+".mscz")
                script(" wget -nv https://ipfs.infura.io"+items[1]+" -O "+items[0])
                downloaded_files.add(int(name))





