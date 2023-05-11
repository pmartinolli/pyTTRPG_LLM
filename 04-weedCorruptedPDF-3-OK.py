# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:11:32 2023

@author: martinop
"""

import os
import shutil
import fitz

from PARAMETERS import folder_path

# Define the name of the subdirectory you want to create for corrupted files
subdirectory = "_corrupted"

# Loop through each file in the directory and its subdirectories
for root, dirs, files in os.walk(folder_path):
    # Exclude directories named "archives" or that start with an underscore "_"
    dirs[:] = [d for d in dirs if d != "archives" and not d.startswith('_')]
    for file in files:
        file_path = os.path.join(root, file)
        if file.endswith('.pdf'):
            pdf_filename = os.path.splitext(file)[0]
            rawtext_file = pdf_filename + ".rawtext"
            yaml_file = pdf_filename + ".yaml"
            ocrtext_file = pdf_filename + ".ocrtext"
            rawtext_file_path = os.path.join(root, rawtext_file)
            yaml_file_path = os.path.join(root, yaml_file)
            ocrtext_file_path = os.path.join(root, ocrtext_file)
        
            try:
                # Try to open the PDF
                with fitz.open(file_path) as pdf:
                    pass
            except (ValueError, RuntimeError):
                # If the PDF can't be opened : 
                # Create the subdirectory if it doesn't already exist
                os.makedirs(os.path.join(folder_path, subdirectory), exist_ok=True)
        
                # then move the files to the subdirectory
                shutil.move(file_path, os.path.join(folder_path, subdirectory, file))
                if os.path.exists(rawtext_file_path):
                    shutil.move(rawtext_file_path, os.path.join(folder_path, subdirectory, rawtext_file))
                if os.path.exists(yaml_file_path):
                    shutil.move(yaml_file_path, os.path.join(folder_path, subdirectory, yaml_file))
                if os.path.exists(ocrtext_file_path):
                    shutil.move(ocrtext_file_path, os.path.join(folder_path, subdirectory, ocrtext_file))
                   
                print("Corrupted moved: ", file)