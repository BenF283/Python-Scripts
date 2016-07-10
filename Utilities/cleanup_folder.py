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
dir_pdf = "Adobe PDFs"
dir_gp = "Guitar Pro Tabs"
dir_media = "Media"
dir_exe = 'Executables'
dir_arch = 'Archives'
dir_misc = 'Miscelaneous'
dir_doc = 'Documents'

#Dictionary storing the file extension and the folder it should be relocated to
#Populate this with the additional extensions and 
locations = {'.iso': dir_iso,
             '.pdf': dir_pdf,
             '.gp5': dir_gp,
             '.gp4': dir_gp,
             '.gp3': dir_gp,
             '.gpx': dir_gp,
             '.midi': dir_gp,
             '.mid': dir_gp,
             '.exe': dir_exe,
             '.msi': dir_exe,
             '.jar': dir_exe,
             '.rar': dir_arch,
             '.zip': dir_arch,
             '.7z': dir_arch,
             '.tar': dir_arch,
             '.gz': dir_arch,
             '.xz': dir_arch,
             '.png': dir_media,
             '.jpg': dir_media,
             '.gif': dir_media,
             '.jpeg': dir_media,
             '.jpg:large': dir_media,
             '.psd': dir_media,
             '.mp4': dir_media,
             '.avi': dir_media,
             '.wav': dir_media,
             '.mp3': dir_media,
             '.dca': dir_media,
             '.txt': dir_misc,
             '.torrent': dir_misc,
             '.sdx': dir_misc,
             '.htm': dir_misc,
             '.doc': dir_doc,
             '.docx': dir_doc,
             '.xls': dir_doc
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
            
