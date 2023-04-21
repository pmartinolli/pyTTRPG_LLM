# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 11:06:50 2023

@author: martinop
"""

import os
import shutil

# Specify the path to the folder containing the files
tested_dir = r'E:/00-Yragatheque/_compilRPGrules/'

# Specify the path to the folder where the PDF files will be saved
destination_dir = r'E:/00-Yragatheque/_compilRPGrules/ocr2do'

# This script will iterate over all files in the pathis directory. 
for filename in os.listdir(tested_dir):
    
    # For each file that has the .rawtext extension,
    if filename.endswith('.rawtext'):
        file_path = os.path.join(tested_dir, filename)
        
        # it will check if its size is less than 1 KB (1024 bytes) 
        if os.path.getsize(file_path) < 1024:
            
            # If it is, the script will check if there is a corresponding .pdf file 
            # with the same name (but with the .pdf extension instead of .rawtext).
            pdf_file = os.path.join(tested_dir, filename.replace('.rawtext', '.pdf'))
            
            # If such a file exists, the script will create a copy of it in the pathos directory.
            if os.path.isfile(pdf_file):
                shutil.copy(pdf_file, destination_dir)
                
            # If such a file exists, the script will delete it.
#            if os.path.isfile(pdf_file):
#                os.remove(pdf_file)                
                