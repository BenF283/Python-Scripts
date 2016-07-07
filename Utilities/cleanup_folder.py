# -*- coding: utf-8 -*-
"""
Created on Thu Jul 07 00:35:17 2016

A simple script to sort files into subfolders. This is useful for Downloads
folders that can get messy with common file types.

To add additional files to move, add the extenstion to the locations dictionary
and add the destination folder as the value.

@author: Ben
"""

import shutil, os

#Folders to sort files in to
dir_iso = "System Images"
dir_pdf = "PDFs"
dir_gp = "Guitar Pro Tabs"
dir_imgs = "Pictures"
dir_exe = 'Executables'
dir_arch = 'Archives'

#Dictionary storing the file extension and the folder it should be relocated to
#Populate this with the additional extensions and 
locations = {'.iso': dir_iso,
             '.pdf': dir_pdf,
             '.gp5': dir_gp,
             '.gp4': dir_gp,
             '.gpx': dir_gp,
             '.exe': dir_exe,
             '.rar': dir_arch,
             '.zip': dir_arch,
             '.7z': dir_arch,
             '.tar': dir_arch,
             '.tar.gz': dir_arch,
             }

#Check if folders exist for tracked files and create them if none exist.
print('Checking folders...\n')
for ext in locations:
    folder = locations.get(ext)    
    try:
        os.stat(folder)
    except:
        print('Making directory for: ' + folder)
        os.mkdir(folder)
    else:
        print(folder + ' already exists.')
        
print('Begining to move files...\n')
countSuccess = 0
countFail = 0

for filename in os.listdir(os.getcwd()):
    try:

        folder = locations.get(os.path.splitext(filename)[1])
        
        if folder != None:
            print('Moving ' + filename + ' to ' + folder)
            shutil.move(filename, os.getcwd() + '\\' + folder)
            countSuccess += 1
    except WindowsError:
        print('Error moving file ' + filename + ', perhaps it is still open?')
        countFail += 1
        
        
print('\n' + str(countSuccess) + ' file(s) have been moved and failed to move ' 
    + str(countFail) + ' file(s). Unlisted extensions have not been moved.')
            
